from __future__ import annotations

from pathlib import Path

from .models import DEFECT_CLASSES, YoloBox


def class_id(name: str) -> int:
    return DEFECT_CLASSES.index(name)


def write_label(path: str | Path, boxes: list[YoloBox]) -> None:
    Path(path).write_text("\n".join(box.to_line() for box in boxes) + ("\n" if boxes else ""), encoding="utf-8")


def split_name(index: int, total: int) -> str:
    ratio = index / max(total, 1)
    if ratio < 0.8:
        return "train"
    if ratio < 0.9:
        return "val"
    return "test"
