"""
Tiny local smoke test for BanglaBERT training pipeline.
Tests gradient accumulation, class weights, early stopping, model save/load, and evaluation.
Runs on CPU with 8 synthetic samples — completes in <2 min after model download.

Usage:
    cd pipelines/BENI/experiment/beni_pilot
    python3 test_banglabert.py
"""

import sys
from pathlib import Path
import numpy as np
import torch
from sklearn.utils.class_weight import compute_class_weight

# Ensure we can import from this directory and the project root
_test_dir = Path(__file__).resolve().parent
_project_root = _test_dir.parents[3]  # goes up to /mnt/data/Projects/nabilox/
sys.path.insert(0, str(_test_dir))
sys.path.insert(0, str(_project_root))

from config import ExperimentConfig
from banglabert import train_banglabert, evaluate_banglabert
from utils import set_seed


def make_synthetic_data(n: int = 8) -> tuple[list[str], list[int]]:
    """Create tiny synthetic Bangla-esque text with 2 classes."""
    rng = np.random.RandomState(42)
    econ_keywords = [
        "অর্থনীতি", "মুদ্রাস্ফীতি", "বাজেট", "জিডিপি", "বিনিয়োগ",
        "রপ্তানি", "রেমিট্যান্স", "বাংলাদেশ ব্যাংক",
    ]
    non_econ_keywords = [
        "ক্রিকেট", "খেলা", "শিক্ষা", "সিনেমা", "রাজনীতি",
        "আবহাওয়া", "স্বাস্থ্য", "বিনোদন",
    ]
    texts, labels = [], []
    for i in range(n):
        pool = econ_keywords if i < n // 2 else non_econ_keywords
        words = pool * (i + 1)
        text = " ".join(words[:10])
        texts.append(text)
        labels.append(1 if i < n // 2 else 0)
    return texts, labels


def test_training_pipeline():
    print("=" * 60)
    print("BanglaBERT Training Pipeline — Smoke Test")
    print("=" * 60)

    set_seed(42)

    # Config with tiny batch, short sequences, and GA
    config = ExperimentConfig(
        seed=42,
        model_name="csebuetnlp/banglabert",  # explicit — default model
        banglabert_epochs=2,
        banglabert_batch_size=2,
        banglabert_max_len=64,
        banglabert_learning_rate=2e-5,
        banglabert_accum_steps=2,  # effective batch = 4
        # Use a temp output directory
        output_dir=Path("/tmp/beni_test/outputs"),
        model_dir=Path("/tmp/beni_test/outputs/models"),
        report_dir=Path("/tmp/beni_test/outputs/reports"),
        banglabert_dir=Path("/tmp/beni_test/banglabert"),
    )
    config.output_dir.mkdir(parents=True, exist_ok=True)
    config.model_dir.mkdir(parents=True, exist_ok=True)
    config.report_dir.mkdir(parents=True, exist_ok=True)

    # Create synthetic data
    texts, labels = make_synthetic_data(8)
    train_texts = texts[:6]
    train_labels = labels[:6]
    val_texts = texts[6:]
    val_labels = labels[6:]

    print(f"\nTrain: {len(train_texts)} samples, Val: {len(val_texts)} samples")
    print(f"  Class distribution — train: {sum(train_labels)}/{len(train_labels)} positive")
    print(f"  Class distribution — val:   {sum(val_labels)}/{len(val_labels)} positive")

    # Compute class weights (same code path as train.py)
    classes = np.array([0, 1])
    cw = compute_class_weight("balanced", classes=classes, y=train_labels)
    class_weight_tensor = torch.tensor(cw, dtype=torch.float)
    print(f"  Class weights: {cw}")

    # ---- Test 1: Training with gradient accumulation ----
    print("\n" + "-" * 40)
    print("Test 1: Training with GA=2, class weights, early stopping")
    print("-" * 40)

    result = train_banglabert(
        config,
        train_texts=train_texts,
        train_labels=train_labels,
        val_texts=val_texts,
        val_labels=val_labels,
        output_name="test_banglabert",
        class_weights=class_weight_tensor,
        gradient_accumulation_steps=config.banglabert_accum_steps,
        model_name=config.model_name,
    )

    print(f"\n  ✓ Training completed")
    print(f"  ✓ History: {len(result['history'])} epochs logged")
    for h in result["history"]:
        print(f"    Epoch {h['epoch']}: loss={h['train_loss']:.4f}  acc={h.get('val_accuracy', 'N/A')}  f1={h.get('val_macro_f1', 'N/A')}")
    print(f"  ✓ Best val macro F1: {result['best_val_macro_f1']:.4f}")
    print(f"  ✓ Model saved to: {result['model_path']}")
    model_dir = Path(result["model_path"])
    assert model_dir.exists(), "Model directory missing"
    # Transformers 4.36+ saves with safetensors by default
    assert (model_dir / "model.safetensors").exists() or (model_dir / "pytorch_model.bin").exists(), "Model weights missing"

    # ---- Test 2: Model evaluation ----
    print("\n" + "-" * 40)
    print("Test 2: Evaluate on test set")
    print("-" * 40)

    eval_result = evaluate_banglabert(
        config,
        test_texts=train_texts,  # reuse train as test (small data)
        test_labels=train_labels,
        model_name="test_banglabert",
    )

    print(f"  ✓ Accuracy:    {eval_result['accuracy']:.4f}")
    print(f"  ✓ Macro F1:    {eval_result['macro_f1']:.4f}")
    print(f"  ✓ Weighted F1: {eval_result['weighted_f1']:.4f}")
    assert "accuracy" in eval_result
    assert "macro_f1" in eval_result

    # ---- Test 3: Early stopping triggers ----
    print("\n" + "-" * 40)
    print("Test 3: Early stopping (should trigger with patience=3)")
    print("-" * 40)

    config_early = ExperimentConfig(
        seed=42,
        banglabert_epochs=10,  # many epochs, but val won't improve (tiny data)
        banglabert_batch_size=2,
        banglabert_max_len=64,
        banglabert_learning_rate=2e-5,
        banglabert_accum_steps=1,
        output_dir=Path("/tmp/beni_test/outputs_early"),
        model_dir=Path("/tmp/beni_test/outputs_early/models"),
        report_dir=Path("/tmp/beni_test/outputs_early/reports"),
        banglabert_dir=Path("/tmp/beni_test/banglabert"),
    )
    config_early.output_dir.mkdir(parents=True, exist_ok=True)
    config_early.model_dir.mkdir(parents=True, exist_ok=True)
    config_early.report_dir.mkdir(parents=True, exist_ok=True)

    result_early = train_banglabert(
        config_early,
        train_texts=train_texts,
        train_labels=train_labels,
        val_texts=val_texts,
        val_labels=val_labels,
        output_name="test_early_stop",
        gradient_accumulation_steps=1,
    )

    epochs_run = len(result_early["history"])
    print(f"  ✓ Requested 10 epochs, actually ran {epochs_run}")
    print(f"  ✓ Best F1: {result_early['best_val_macro_f1']:.4f}")
    # Early stopping should have triggered before 10
    assert epochs_run < 10, f"Early stopping did not trigger! Ran all {epochs_run} epochs"
    print(f"  ✓ PASS: Early stopping triggered at epoch {epochs_run}")

    # ---- Summary ----
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)

    # Cleanup
    import shutil
    for d in ["/tmp/beni_test"]:
        shutil.rmtree(d, ignore_errors=True)
    print("Temp files cleaned up.")


if __name__ == "__main__":
    test_training_pipeline()
