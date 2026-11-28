#!/usr/bin/env python3
"""Validate GovCheck formal JSON Schemas and their synthetic example fixtures.

This checks Draft 2020-12 schema validity and fixture conformance only. It does
not establish semantic correctness, authority, provenance truth, or assurance.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

SCHEMA_DIRS = (
    Path("formal/schemas"),
    Path("govcheck/formal/schemas"),
    Path("docs/schemas"),
)
FIXTURE_DIR = Path("formal/fixtures")


class ValidationSetupError(ValueError):
    pass


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationSetupError(f"{path}: cannot read JSON: {exc}") from exc


def fixture_schema_name(name: str) -> str | None:
    if name == "dependency-edge.example.json":
        return "formal/schemas/dependency-edge.schema.json"
    if name.startswith("evidence-record-") and name.endswith(".example.json"):
        return "formal/schemas/evidence-record.schema.json"
    if name.startswith("version-decision-") and name.endswith(".example.json"):
        return "formal/schemas/version-decision.schema.json"
    if name == "release-manifest.example.json":
        return "formal/schemas/release-manifest.schema.json"
    if name == "version-governance-bundle.example.json":
        return "formal/schemas/version-governance-bundle.schema.json"
    return None


def load_schemas(root: str | Path) -> tuple[dict[str, dict], Registry]:
    root = Path(root).resolve()
    schemas: dict[str, dict] = {}
    resources = []
    schema_by_id: dict[str, dict] = {}
    for relative_directory in SCHEMA_DIRS:
        directory = root / relative_directory
        if not directory.is_dir():
            raise ValidationSetupError(f"schema directory does not exist: {directory}")
        for path in sorted(directory.glob("*.schema.json")):
            schema = _read_json(path)
            if not isinstance(schema, dict):
                raise ValidationSetupError(f"{path}: schema root must be an object")
            schema_id = schema.get("$id")
            if not isinstance(schema_id, str) or not schema_id:
                raise ValidationSetupError(f"{path}: schema must declare a non-empty $id")
            key = path.relative_to(root).as_posix()
            if key in schemas:
                raise ValidationSetupError(f"duplicate schema path: {key}")
            Draft202012Validator.check_schema(schema)
            schemas[key] = schema
            previous = schema_by_id.get(schema_id)
            if previous is not None:
                if previous != schema:
                    raise ValidationSetupError(
                        f"duplicate schema $id has conflicting contents: {schema_id}"
                    )
                # Documentation and package projections may intentionally share
                # one canonical schema ID. Register that resource only once.
                continue
            schema_by_id[schema_id] = schema
            resources.append((schema_id, Resource.from_contents(schema)))
    if not schemas:
        raise ValidationSetupError("no *.schema.json files found")
    registry = Registry().with_resources(resources)
    return schemas, registry


def validate_instance(instance: Any, schema: dict, registry: Registry, path: str) -> list[dict[str, str]]:
    validator = Draft202012Validator(
        schema, registry=registry, format_checker=FormatChecker()
    )
    errors = sorted(validator.iter_errors(instance), key=lambda error: (list(map(str, error.absolute_path)), error.message))
    return [
        {
            "instance": path,
            "location": "/" + "/".join(str(part) for part in error.absolute_path),
            "message": error.message,
        }
        for error in errors
    ]


def audit(root: str | Path) -> dict:
    root = Path(root).resolve()
    schemas, registry = load_schemas(root)
    fixtures_dir = root / FIXTURE_DIR
    if not fixtures_dir.is_dir():
        raise ValidationSetupError(f"fixture directory does not exist: {fixtures_dir}")

    findings: list[dict[str, str]] = []
    fixture_count = 0
    covered: set[str] = set()
    for path in sorted(fixtures_dir.glob("*.example.json")):
        schema_name = fixture_schema_name(path.name)
        if schema_name is None:
            findings.append({
                "instance": path.relative_to(root).as_posix(),
                "location": "",
                "message": "fixture has no explicit schema mapping",
            })
            continue
        if schema_name not in schemas:
            findings.append({
                "instance": path.relative_to(root).as_posix(),
                "location": "",
                "message": f"mapped schema is missing: {schema_name}",
            })
            continue
        fixture_count += 1
        covered.add(schema_name)
        try:
            instance = _read_json(path)
        except ValidationSetupError as exc:
            findings.append({"instance": path.relative_to(root).as_posix(), "location": "", "message": str(exc)})
            continue
        findings.extend(validate_instance(
            instance, schemas[schema_name], registry, path.relative_to(root).as_posix()
        ))

    fixture_required = {name for name in schemas if name.startswith("formal/schemas/")}
    for schema_name in sorted(fixture_required - covered):
        findings.append({
            "instance": "",
            "location": "",
            "message": f"schema has no mapped example fixture: {schema_name}",
        })

    return {
        "format": "govcheck.formal-json-schema-validation/v1",
        "status": "invalid" if findings else "valid",
        "json_schema_validation_performed": True,
        "dialect": "https://json-schema.org/draft/2020-12/schema",
        "schemas_checked": len(schemas),
        "formal_schemas_checked": sum(name.startswith("formal/schemas/") for name in schemas),
        "package_schemas_checked": sum(name.startswith("govcheck/formal/schemas/") for name in schemas),
        "documentation_schemas_checked": sum(name.startswith("docs/schemas/") for name in schemas),
        "fixtures_checked": fixture_count,
        "fixture_coverage_scope": "Example fixtures are currently required for formal/schemas; packaged and documentation schemas are meta-validated and registered for cross-reference resolution, but are not yet fixture-covered.",
        "finding_count": len(findings),
        "findings": findings,
        "limitations": [
            "Schema and fixture validation checks structure and declared formats only.",
            "A valid fixture is synthetic and is not evidence about repository behavior.",
            "Cross-record semantic checks, authority resolution, provenance authenticity and assurance remain separate.",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = audit(args.root)
    except ValidationSetupError as exc:
        print(f"Formal JSON Schema validation could not complete: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
