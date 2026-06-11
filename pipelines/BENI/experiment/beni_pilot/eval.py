from __future__ import annotations

import argparse

import joblib
from config import ExperimentConfig
from data import add_economic_relevance_label, load_split
from utils import write_json

from pipelines.shared.eval import evaluate_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a trained BENI pilot model.")
    parser.add_argument("--task", choices=["topic", "economic"], default="topic")
    parser.add_argument("--split", choices=["dev", "test"], default="test")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = ExperimentConfig(target_task=args.task)
    model_path = config.model_dir / f"{args.task}_tfidf_logreg.joblib"
    model = joblib.load(model_path)
    frame = add_economic_relevance_label(load_split(config, args.split))
    target = "class_label" if args.task == "topic" else "economic_relevance"
    report = evaluate_model(model, frame["text_norm"], frame[target])
    out_path = config.report_dir / f"{args.task}_{args.split}_eval.json"
    write_json(out_path, report)
    print(f"saved_report={out_path}")


if __name__ == "__main__":
    main()
