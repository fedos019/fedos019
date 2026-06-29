from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import isclose
from pathlib import Path

from .models import MeshReport


@dataclass(slots=True)
class ObjMesh:
    vertices: list[tuple[float, float, float]]
    faces: list[tuple[int, ...]]

    @classmethod
    def load(cls, path: str | Path) -> "ObjMesh":
        vertices: list[tuple[float, float, float]] = []
        faces: list[tuple[int, ...]] = []
        with Path(path).open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("v "):
                    _, x, y, z, *_ = line.split()
                    vertices.append((float(x), float(y), float(z)))
                elif line.startswith("f "):
                    indexes = []
                    for token in line.split()[1:]:
                        raw = token.split("/", 1)[0]
                        index = int(raw)
                        indexes.append(index - 1 if index > 0 else len(vertices) + index)
                    faces.append(tuple(indexes))
        return cls(vertices=vertices, faces=faces)

    def validate(self) -> MeshReport:
        duplicate_vertices = len(self.vertices) - len(set(self.vertices))
        edge_counter: Counter[tuple[int, int]] = Counter()
        degenerate_faces = 0
        for face in self.faces:
            if len(face) < 3 or len(set(face)) != len(face):
                degenerate_faces += 1
                continue
            for left, right in zip(face, face[1:] + face[:1]):
                edge_counter[tuple(sorted((left, right)))] += 1
        open_edges = sum(1 for count in edge_counter.values() if count == 1)
        non_manifold = sum(1 for count in edge_counter.values() if count > 2)
        bounds = self.bounds()
        recommendations: list[str] = []
        if open_edges:
            recommendations.append("Обнаружены открытые границы: проверьте непросканированные области и технологические отверстия.")
        if duplicate_vertices:
            recommendations.append("Обнаружены дублирующиеся вершины: выполните weld/merge перед генерацией.")
        if non_manifold:
            recommendations.append("Mesh не является manifold: исправьте ребра, принадлежащие более чем двум граням.")
        if degenerate_faces:
            recommendations.append("Удалите вырожденные полигоны перед экспортом датасета.")
        if self._has_zero_extent(bounds):
            recommendations.append("Проверьте масштаб и систему координат: одна из размерностей равна нулю.")
        return MeshReport(len(self.vertices), len(self.faces), duplicate_vertices, open_edges, non_manifold, degenerate_faces, bounds, recommendations)

    def bounds(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        if not self.vertices:
            return ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        xs, ys, zs = zip(*self.vertices)
        return ((min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs)))

    @staticmethod
    def _has_zero_extent(bounds: tuple[tuple[float, float, float], tuple[float, float, float]]) -> bool:
        return any(isclose(high - low, 0.0) for low, high in zip(bounds[0], bounds[1]))
