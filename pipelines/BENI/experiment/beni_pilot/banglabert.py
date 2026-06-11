from __future__ import annotations

import gc
import math
import sys
from pathlib import Path
from typing import Any, Optional

import numpy as np
import torch
from sklearn.metrics import accuracy_score, classification_report, f1_score, roc_auc_score
from torch.cuda.amp import GradScaler, autocast
from torch.utils.data import DataLoader, Dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    get_linear_schedule_with_warmup,
)

from config import ExperimentConfig
from utils import write_json


MODEL_REGISTRY: dict[str, dict] = {
    "csebuetnlp/banglabert_small": {
        "params": 13_000_000, "default_batch": 32, "default_max_len": 384
    },
    "csebuetnlp/banglabert": {
        "params": 110_000_000, "default_batch": 8, "default_max_len": 384
    },
    "sagorsarker/bangla-bert-base": {
        "params": 110_000_000, "default_batch": 8, "default_max_len": 384
    },
    "neuropark/sahajBERT": {
        "params": 18_000_000, "default_batch": 32, "default_max_len": 384
    },
    "xlm-roberta-base": {
        "params": 270_000_000, "default_batch": 8, "default_max_len": 384
    },
    "bert-base-multilingual-cased": {
        "params": 180_000_000, "default_batch": 8, "default_max_len": 384
    },
}


def get_model_short_name(model_name: str) -> str:
    mapping = {
        "csebuetnlp/banglabert_small": "banglabert_small",
        "csebuetnlp/banglabert": "banglabert",
        "sagorsarker/bangla-bert-base": "bangla_bert_base",
        "neuropark/sahajBERT": "sahajbert",
        "xlm-roberta-base": "xlm_roberta_base",
        "bert-base-multilingual-cased": "mbert",
    }
    return mapping.get(model_name, model_name.replace("/", "_").replace("-", "_"))


def _load_tokenizer_and_model(
    model_name: str,
    cache_dir: Path | None = None,
    num_labels: int = 2,
):
    if cache_dir is not None and cache_dir.exists():
        print(f"Loading {model_name} from local cache: {cache_dir}", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(str(cache_dir))
        model = AutoModelForSequenceClassification.from_pretrained(
            str(cache_dir),
            num_labels=num_labels,
            ignore_mismatched_sizes=True,
        )
    else:
        print(f"Local cache not found at {cache_dir}, downloading {model_name} from HuggingFace hub...", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels,
            ignore_mismatched_sizes=True,
        )
        if cache_dir is not None:
            cache_dir.mkdir(parents=True, exist_ok=True)
            tokenizer.save_pretrained(str(cache_dir))
            model.save_pretrained(str(cache_dir))
            print(f"Cached {model_name} to {cache_dir}", flush=True)
    return tokenizer, model


class BanglaBERTDataset(Dataset):
    def __init__(self, texts: list[str], labels: list[int], tokenizer, config: ExperimentConfig):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = config.banglabert_max_len

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(self.labels[idx], dtype=torch.long),
        }


def _predict(model, dataloader: DataLoader, device: torch.device) -> tuple[np.ndarray, np.ndarray]:
    model.eval()
    all_preds, all_probs, all_labels = [], [], []
    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            probs = torch.softmax(outputs.logits, dim=-1)
            preds = torch.argmax(outputs.logits, dim=-1)
            all_preds.extend(preds.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    return np.array(all_preds), np.array(all_probs), np.array(all_labels)


def train_banglabert(
    config: ExperimentConfig,
    train_texts: list[str],
    train_labels: list[int],
    val_texts: list[str] | None = None,
    val_labels: list[int] | None = None,
    output_name: str | None = None,
    class_weights: torch.Tensor | None = None,
    gradient_accumulation_steps: int | None = None,
    model_name: str = "csebuetnlp/banglabert",
) -> dict[str, Any]:
    if output_name is None:
        output_name = f"{get_model_short_name(model_name)}_economic"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device={device}", flush=True)

    model_cache_dir = config.banglabert_dir / get_model_short_name(model_name)
    tokenizer, model = _load_tokenizer_and_model(
        model_name=model_name,
        cache_dir=model_cache_dir,
        num_labels=len(set(train_labels)) if train_labels else 2,
    )
    model.to(device)

    use_amp = device.type == "cuda" and torch.cuda.get_device_capability() >= (7, 0)
    scaler = GradScaler(enabled=use_amp)
    print(f"fp16={use_amp} (device_cap={torch.cuda.get_device_capability() if device.type == 'cuda' else 'N/A'})", flush=True)

    weight_on_device = class_weights.to(device) if class_weights is not None else None
    ce_loss_fn = torch.nn.CrossEntropyLoss(weight=weight_on_device)

    gpu_workers = 2 if device.type == "cuda" else 0
    pin_memory = device.type == "cuda"

    train_dataset = BanglaBERTDataset(train_texts, train_labels, tokenizer, config)
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.banglabert_batch_size,
        shuffle=True,
        num_workers=gpu_workers,
        pin_memory=pin_memory,
    )

    # Gradient accumulation: if not set, default to config value or 1
    if gradient_accumulation_steps is None:
        gradient_accumulation_steps = config.banglabert_accum_steps
    effective_batch = config.banglabert_batch_size * gradient_accumulation_steps
    print(f"train_loader batches={len(train_loader)} batch_size={config.banglabert_batch_size}", flush=True)
    print(f"gradient_accumulation_steps={gradient_accumulation_steps} effective_batch_size={effective_batch}", flush=True)

    optimizer = torch.optim.AdamW(model.parameters(), lr=config.banglabert_learning_rate)

    optimizer_steps_per_epoch = math.ceil(len(train_loader) / gradient_accumulation_steps)
    total_optimizer_steps = optimizer_steps_per_epoch * config.banglabert_epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=int(0.1 * total_optimizer_steps),
        num_training_steps=total_optimizer_steps,
    )

    patience = 3
    patience_counter = 0
    best_val_f1 = 0.0
    best_epoch = 0
    best_state = None
    history = []

    val_loader = None
    if val_texts is not None and val_labels is not None:
        val_dataset = BanglaBERTDataset(val_texts, val_labels, tokenizer, config)
        val_loader = DataLoader(
            val_dataset,
            batch_size=config.banglabert_batch_size,
            shuffle=False,
            pin_memory=pin_memory,
        )

    for epoch in range(config.banglabert_epochs):
        model.train()
        total_loss = 0
        optimizer.zero_grad()

        for step, batch in enumerate(train_loader):
            input_ids = batch["input_ids"].to(device, non_blocking=True)
            attention_mask = batch["attention_mask"].to(device, non_blocking=True)
            labels = batch["labels"].to(device, non_blocking=True)

            with autocast(enabled=use_amp):
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                # Normalize loss by accumulation steps so gradients sum correctly
                loss = ce_loss_fn(outputs.logits, labels) / gradient_accumulation_steps

            scaler.scale(loss).backward()

            if (step + 1) % gradient_accumulation_steps == 0 or (step + 1) == len(train_loader):
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                scaler.step(optimizer)
                scaler.update()
                scheduler.step()
                optimizer.zero_grad()

            total_loss += loss.item() * gradient_accumulation_steps

            if step > 0 and step % 500 == 0:
                mem = torch.cuda.memory_allocated() / 1024**2 if device.type == "cuda" else 0
                print(f"    step {step}/{len(train_loader)} loss={loss.item() * gradient_accumulation_steps:.4f} gpu_mem={mem:.0f}MiB", flush=True)

        avg_loss = total_loss / len(train_loader)

        val_metrics = {}
        if val_loader is not None and val_labels is not None:
            preds, probs, true = _predict(model, val_loader, device)
            val_f1 = float(f1_score(true, preds, average="macro"))
            val_acc = float(accuracy_score(true, preds))
            val_auc = float(roc_auc_score(true, probs[:, 1]))
            val_metrics = {"val_accuracy": val_acc, "val_macro_f1": val_f1, "val_auc_roc": val_auc}

            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                best_epoch = epoch + 1
                best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
                patience_counter = 0
            else:
                patience_counter += 1
                print(f"    early stopping patience {patience_counter}/{patience} (best F1={best_val_f1:.4f} @ epoch {best_epoch})", flush=True)

        epoch_result = {"epoch": epoch + 1, "train_loss": round(avg_loss, 4), **val_metrics}
        history.append(epoch_result)
        mem = torch.cuda.memory_allocated() / 1024**2 if device.type == "cuda" else 0
        print(f"  epoch {epoch+1}: loss={avg_loss:.4f} {val_metrics} gpu_mem={mem:.0f}MiB", flush=True)

        if patience_counter >= patience:
            print(f"  Early stopping triggered at epoch {epoch+1}. Best epoch {best_epoch} (F1={best_val_f1:.4f})", flush=True)
            break

    # Restore best model
    if best_state is not None:
        model.load_state_dict(best_state)

    # Save model
    save_path = config.model_dir / output_name
    model.save_pretrained(str(save_path))
    tokenizer.save_pretrained(str(save_path))
    print(f"model saved: {save_path}")

    # Cleanup GPU memory
    del model
    gc.collect()
    torch.cuda.empty_cache()

    return {
        "output_name": output_name,
        "model_path": str(save_path),
        "history": history,
        "best_val_macro_f1": best_val_f1,
        "epochs": config.banglabert_epochs,
        "batch_size": config.banglabert_batch_size,
        "learning_rate": config.banglabert_learning_rate,
    }


def evaluate_banglabert(
    config: ExperimentConfig,
    test_texts: list[str],
    test_labels: list[int],
    model_name: str = "banglabert_economic",
) -> dict[str, Any]:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_path = config.model_dir / model_name
    tokenizer = AutoTokenizer.from_pretrained(str(model_path))
    model = AutoModelForSequenceClassification.from_pretrained(str(model_path))
    model.to(device)
    model.eval()

    dataset = BanglaBERTDataset(test_texts, test_labels, tokenizer, config)
    loader = DataLoader(dataset, batch_size=config.banglabert_batch_size, shuffle=False)

    preds, probs, true = _predict(model, loader, device)

    report = {
        "accuracy": float(accuracy_score(true, preds)),
        "macro_f1": float(f1_score(true, preds, average="macro")),
        "weighted_f1": float(f1_score(true, preds, average="weighted")),
        "classification_report": classification_report(true, preds, output_dict=True, zero_division=0),
    }

    del model
    gc.collect()
    torch.cuda.empty_cache()

    return report
