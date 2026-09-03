#!/usr/bin/env python3
"""Export versioned read-model projections from the rich local SIIAOS registry.

Stdlib only. No network access. No command execution.

Important boundary:
- radar-public.json is genuinely public and must not contain data hidden only by UI;
- consultant-site.json is an explicitly publishable editorial projection;
- contextual Expert data remains local/protected and is not written as a public static file here.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_CONSULTANT = "siiaos.consultant-qualification.v1"
SCHEMA_RADAR = "siiaos.radar-public.v1"


def load_records(root: Path) -> Iterable[dict[str, Any]]:
    for path in sorted(root.rglob("*.json")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(raw, dict) and raw.get("id") and raw.get("publication"):
            yield raw


def choose_fit(record: dict[str, Any], context: str) -> dict[str, Any] | None:
    fits = record.get("fit") or []
    exact = [item for item in fits if isinstance(item, dict) and item.get("context") == context]
    if exact:
        return exact[0]
    valid = [item for item in fits if isinstance(item, dict) and isinstance(item.get("score"), (int, float))]
    return max(valid, key=lambda item: item.get("score", 0), default=None)


def consultant_item(record: dict[str, Any], radar_base_url: str, fit_context: str) -> tuple[str, dict[str, Any]] | None:
    """Build the explicitly publishable consultant-site projection.

    This remains separate from radar-public. A record is exported only when the
    canonical publication gate explicitly enables consultant_site and supplies
    a stable consultant_slug.
    """
    publication = record.get("publication") or {}
    if not publication.get("consultant_site"):
        return None
    projection_keys = record.get("projection_keys") or {}
    slug = projection_keys.get("consultant_slug")
    if not slug:
        return None

    fit = choose_fit(record, fit_context)
    trend = record.get("trend") or {}
    evidence_ids = record.get("evidence_ids") or []
    radar_slug = projection_keys.get("radar_slug") or record.get("id")
    item: dict[str, Any] = {
        "canonical_id": record["id"],
        "competitive_position": record.get("competitive_position", "unknown"),
        "source_state": record.get("state"),
        "last_verified_at": record.get("last_verified_at"),
        "verified_on": record.get("verified_on") or [],
        "benchmark_summary": record.get("benchmark_summary"),
        "known_gaps": record.get("known_gaps") or [],
        "radar_url": f"{radar_base_url.rstrip('/')}/#resource/{radar_slug}",
        "evidence_count": len(evidence_ids),
        "trend_30d": trend.get("delta_30d"),
    }
    if fit:
        item.update(
            {
                "fit_score": fit.get("score"),
                "fit_confidence": fit.get("confidence"),
                "fit_context": fit.get("context"),
            }
        )
    return slug, {key: value for key, value in item.items() if value is not None}


def radar_item(record: dict[str, Any]) -> dict[str, Any] | None:
    """Build the truly public/free Radar projection.

    Never expose contextual fit scores, competitive ranking, detailed benchmark
    conclusions, client-specific architecture or other values that are meant to
    require an authenticated Expert session.
    """
    publication = record.get("publication") or {}
    if not publication.get("radar_public"):
        return None

    allowed = (
        "id",
        "kind",
        "title",
        "summary",
        "source_url",
        "repo_url",
        "capabilities",
        "approaches",
        "state",
        "maturity",
        "license",
        "last_activity",
        "last_verified_at",
        "verified_on",
        "trend",
        "known_gaps",
        "replaces",
        "competes_with",
        "depends_on",
        "enables",
        "updated_at",
    )
    item = {key: record[key] for key in allowed if key in record}

    evidence_ids = record.get("evidence_ids") or []
    fits = [entry for entry in (record.get("fit") or []) if isinstance(entry, dict)]
    item["expert_available"] = {
        "evidence_count": len(evidence_ids),
        "benchmark": bool(record.get("benchmark_summary")),
        "fit": bool(fits),
        "contextual_position": record.get("competitive_position") not in (None, "", "unknown"),
    }
    return item


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True, help="Canonical registry directory")
    parser.add_argument("--out", required=True, help="Projection output directory")
    parser.add_argument("--fit-context", default="sandy", help="Preferred fit context for consultant projection")
    parser.add_argument("--radar-base-url", default="https://siiaos-resource-radar.vercel.app")
    args = parser.parse_args()

    registry = Path(args.registry).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    consultant: dict[str, Any] = {}
    radar: list[dict[str, Any]] = []
    skipped_consultant_without_slug: list[str] = []

    records = list(load_records(registry))
    for record in records:
        if (record.get("publication") or {}).get("consultant_site"):
            item = consultant_item(record, args.radar_base_url, args.fit_context)
            if item:
                slug, payload = item
                consultant[slug] = payload
            else:
                skipped_consultant_without_slug.append(str(record.get("id")))
        public_item = radar_item(record)
        if public_item:
            radar.append(public_item)

    write_json(
        out / "consultant-site.json",
        {"schema": SCHEMA_CONSULTANT, "generatedAt": generated_at, "items": consultant},
    )
    write_json(
        out / "radar-public.json",
        {"schema": SCHEMA_RADAR, "generatedAt": generated_at, "items": radar},
    )
    write_json(
        out / "export-report.json",
        {
            "generatedAt": generated_at,
            "canonical_records": len(records),
            "consultant_items": len(consultant),
            "radar_items": len(radar),
            "consultant_missing_projection_key": skipped_consultant_without_slug,
            "expert_static_projection_written": False,
            "public_projection_excludes": [
                "fit",
                "competitive_position",
                "benchmark_summary",
                "blast_radius",
            ],
        },
    )
    print(f"SIIAOS projections: {len(consultant)} consultant, {len(radar)} radar public")
    print("Expert contextual data: kept out of public static projection")
    if skipped_consultant_without_slug:
        print(f"WARNING: {len(skipped_consultant_without_slug)} consultant record(s) missing consultant_slug")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
