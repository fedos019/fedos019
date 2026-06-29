from pathlib import Path

from turbine_blade_suite.defects import generate_defects
from turbine_blade_suite.expert import evaluate
from turbine_blade_suite.obj_mesh import ObjMesh
from turbine_blade_suite.projects import create_project
from turbine_blade_suite.yolo import YoloBox, split_name
from turbine_blade_suite.zones import validate_zones
from turbine_blade_suite.models import Zone


def test_obj_validation_finds_open_edges_and_duplicates(tmp_path: Path) -> None:
    obj = tmp_path / "blade.obj"
    obj.write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nv 0 1 0\nf 1 2 3\n", encoding="utf-8")
    report = ObjMesh.load(obj).validate()
    assert report.vertex_count == 4
    assert report.face_count == 1
    assert report.duplicate_vertices == 1
    assert report.open_boundary_edges == 3


def test_project_scaffold_and_dataset_split(tmp_path: Path) -> None:
    project = create_project(tmp_path / "p", "Demo", "blade-a")
    assert (project.root / "config.json").exists()
    assert (project.root / "dataset/labels/test").is_dir()
    assert split_name(80, 100) == "val"
    assert split_name(95, 100) == "test"


def test_zone_validation_yolo_and_rules() -> None:
    errors = validate_zones({"пера": Zone("пера", "#fff", [1, 2]), "замок": Zone("замок", "#000", [2])})
    assert errors
    assert YoloBox(0, 0.5, 0.5, 0.2, 0.1).to_line() == "0 0.500000 0.500000 0.200000 0.100000"
    assert evaluate({"zone": "перо", "type": "crack", "area": 12}, [{"type": "crack", "min_area": 10, "decision": "брак"}]) == "брак"


def test_defect_generation_is_seeded() -> None:
    rules = [{"type": "crack", "zone": "перо", "count": [2, 2], "length": [1, 1], "width": [2, 2]}]
    defects = generate_defects(rules, seed=1)
    assert len(defects) == 2
    assert defects[0].area == 2
