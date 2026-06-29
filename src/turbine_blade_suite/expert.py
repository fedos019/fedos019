from __future__ import annotations

from typing import Any


def evaluate(defect: dict[str, Any], rules: list[dict[str, Any]]) -> str:
    for rule in rules:
        if rule.get("zone") not in (None, defect.get("zone")):
            continue
        if rule.get("type") not in (None, defect.get("type")):
            continue
        max_area = rule.get("max_area")
        min_area = rule.get("min_area")
        area = float(defect.get("area", 0))
        if max_area is not None and area > max_area:
            continue
        if min_area is not None and area < min_area:
            continue
        return rule["decision"]
    return "дополнительная проверка"
