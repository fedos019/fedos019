from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFECT_CLASSES = ["crack", "dent", "chip", "rust", "corrosion", "erosion", "scratch", "wear"]


@dataclass(slots=True)
class ScaleInfo:
    length_mm: float = 0.0
    width_mm: float = 0.0
    height_mm: float = 0.0
    obj_units_per_mm: float = 1.0
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    axes: dict[str, str] = field(default_factory=lambda: {"X": "leading_to_trailing", "Y": "thickness", "Z": "blade_span"})


@dataclass(slots=True)
class Project:
    name: str
    description: str
    blade_type: str
    root: Path
    obj_model: Path | None = None
    zones_file: Path | None = None
    scale: ScaleInfo = field(default_factory=ScaleInfo)
    camera: dict[str, Any] = field(default_factory=dict)
    lighting: dict[str, Any] = field(default_factory=dict)
    generation: dict[str, Any] = field(default_factory=dict)
    export: dict[str, Any] = field(default_factory=dict)
    changelog: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class MeshReport:
    vertex_count: int
    face_count: int
    duplicate_vertices: int
    open_boundary_edges: int
    non_manifold_edges: int
    degenerate_faces: int
    bounds: tuple[tuple[float, float, float], tuple[float, float, float]]
    recommendations: list[str]


@dataclass(frozen=True, slots=True)
class Zone:
    name: str
    color: str
    faces: list[int]


@dataclass(frozen=True, slots=True)
class Defect:
    defect_type: str
    zone: str
    center: tuple[float, float, float]
    length: float
    width: float
    depth: float
    area: float
    direction_deg: float
    color: str
    roughness: float


@dataclass(frozen=True, slots=True)
class YoloBox:
    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float

    def to_line(self) -> str:
        values = [self.x_center, self.y_center, self.width, self.height]
        if any(value < 0 or value > 1 for value in values):
            raise ValueError("YOLO coordinates must be normalized to [0, 1]")
        return f"{self.class_id} " + " ".join(f"{value:.6f}" for value in values)
