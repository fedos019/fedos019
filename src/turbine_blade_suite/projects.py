from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import Project, ScaleInfo

PROJECT_FILES = ["blade.obj", "zones.json", "config.json", "camera.json", "lighting.json", "generation.json"]


def create_project(root: str | Path, name: str, blade_type: str, description: str = "") -> Project:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    project = Project(name=name, description=description, blade_type=blade_type, root=root)
    for folder in ["assets", "reports", "dataset/images/train", "dataset/images/val", "dataset/images/test", "dataset/labels/train", "dataset/labels/val", "dataset/labels/test"]:
        (root / folder).mkdir(parents=True, exist_ok=True)
    save_json(root / "config.json", {"name": name, "description": description, "blade_type": blade_type, "scale": asdict(project.scale), "changelog": ["Project created"]})
    save_json(root / "camera.json", default_camera())
    save_json(root / "lighting.json", default_lighting())
    save_json(root / "generation.json", default_generation())
    save_json(root / "zones.json", {"version": 1, "zones": []})
    return project


def save_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def default_camera() -> dict:
    return {"position": [0, -350, 120], "target": [0, 0, 80], "focal_length_mm": 50, "depth_of_field": {"enabled": True, "f_stop": 5.6}}


def default_lighting() -> dict:
    return {"sources": [{"type": "area", "power_w": 450, "temperature_k": 5600}], "randomize": {"position": True, "temperature_k": [4200, 7000]}}


def default_generation() -> dict:
    return {"split": {"train": 0.8, "val": 0.1, "test": 0.1}, "domain_randomization": True, "defect_classes": ["crack", "dent", "chip", "rust", "corrosion", "erosion", "scratch", "wear"]}
