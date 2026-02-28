"""Parse exam.yaml into an ExamConfig model."""

from __future__ import annotations

from pathlib import Path

import yaml

from cert_pepper.models.content import ExamConfig


def parse_exam_yaml(path: Path) -> ExamConfig:
    """Parse exam.yaml at *path* and return an ExamConfig.

    Raises:
        FileNotFoundError: if *path* does not exist.
        ValueError: if required fields are missing or weights don't sum to 100.
    """
    if not path.exists():
        raise FileNotFoundError(f"exam.yaml not found at {path}")

    with path.open() as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"exam.yaml at {path} must be a YAML mapping")

    config = ExamConfig(**data)

    total = sum(d.weight_pct for d in config.domains)
    if abs(total - 100.0) > 0.1:
        raise ValueError(
            f"Domain weights in {path} sum to {total:.1f}%, expected 100.0%"
        )

    return config
