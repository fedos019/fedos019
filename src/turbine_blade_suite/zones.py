from __future__ import annotations

import json
from pathlib import Path

from .models import Zone


def load_zones(path: str | Path) -> dict[str, Zone]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return {item["name"]: Zone(name=item["name"], color=item.get("color", "#cccccc"), faces=item.get("faces", [])) for item in payload.get("zones", [])}


def validate_zones(zones: dict[str, Zone]) -> list[str]:
    owners: dict[int, str] = {}
    errors: list[str] = []
    for zone in zones.values():
        for face in zone.faces:
            if face in owners:
                errors.append(f"Polygon {face} belongs to both {owners[face]} and {zone.name}")
            owners[face] = zone.name
    return errors
