from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .obj_mesh import ObjMesh
from .projects import create_project


def main() -> None:
    parser = argparse.ArgumentParser(description="Turbine blade synthetic dataset toolkit")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init-project")
    init.add_argument("root")
    init.add_argument("name")
    init.add_argument("blade_type")
    validate = sub.add_parser("validate-obj")
    validate.add_argument("obj")
    args = parser.parse_args()
    if args.command == "init-project":
        project = create_project(args.root, args.name, args.blade_type)
        print(json.dumps({"root": str(project.root), "name": project.name}, ensure_ascii=False))
    elif args.command == "validate-obj":
        report = ObjMesh.load(args.obj).validate()
        print(json.dumps(asdict(report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
