from __future__ import annotations

import random
from typing import Any

from .models import DEFECT_CLASSES, Defect


def generate_defects(rules: list[dict[str, Any]], seed: int | None = None) -> list[Defect]:
    rng = random.Random(seed)
    defects: list[Defect] = []
    for rule in rules:
        defect_type = rule["type"]
        if defect_type not in DEFECT_CLASSES:
            raise ValueError(f"Unknown defect type: {defect_type}")
        count = rng.randint(*rule.get("count", [1, 1]))
        for _ in range(count):
            length = _uniform(rng, rule.get("length", [1.0, 5.0]))
            width = _uniform(rng, rule.get("width", [0.2, 2.0]))
            defects.append(Defect(defect_type, rule.get("zone", "перо"), tuple(_uniform(rng, axis) for axis in rule.get("coordinates", [[0, 0], [0, 0], [0, 0]])), length, width, _uniform(rng, rule.get("depth", [0.0, 1.0])), length * width, _uniform(rng, rule.get("direction_deg", [0, 180])), rule.get("color", "#663300"), _uniform(rng, rule.get("roughness", [0.1, 0.8]))))
    return defects


def _uniform(rng: random.Random, bounds: list[float]) -> float:
    return rng.uniform(float(bounds[0]), float(bounds[1]))
