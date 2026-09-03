#!/usr/bin/env python3
"""SIIAOS Local Bridge V4.

Localhost-only bridge for governed downloads, manifest ingestion, structured
observations and read-only public projections. Python stdlib only.

Security posture:
- binds to 127.0.0.1 only;
- token required for every endpoint except minimal /health;
- no shell/command execution endpoint;
- HTTP(S) downloads only;
- blocks loopback/link-local/private/reserved targets by default, including
  redirect targets, to prevent the public Radar from becoming an SSRF proxy;
- root-confined file writes with atomic .part downloads;
- configurable batch, size and concurrency limits;
- explicit CORS allowlist.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import re
import secrets
import socket
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

VERSION = "4.0.0-alpha.1"
USER_AGENT = f"SIIAOS-Local-Bridge/{VERSION}"
TASKS: dict[str, dict[str, Any]] = {}
TASK_LOCK = threading.Lock()


def safe_name(value: str | None, fallback: str = "artifact.bin") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._()\- +@]+", "_", value or fallback).strip(" .")[:220]
    return cleaned or fallback


def safe_target(root: Path, subdir: str | None, filename: str | None) -> Path:
    root = root.resolve()
    safe_parts = [safe_name(part, "_") for part in Path(subdir or "").parts if part not in (".", "..")]
    target = (root.joinpath(*safe_parts) / safe_name(filename)).resolve()
    if target != root and root not in target.parents:
        raise ValueError("destination hors racine")
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def append_event(log_path: Path, event: dict[str, Any]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps({"ts": time.time(), **event}, ensure_ascii=False)
    with open(log_path, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def resolve_public_host(hostname: str, allow_private_hosts: set[str]) -> None:
    normalized = hostname.rstrip(".").lower()
    if normalized in allow_private_hosts:
        return
    try:
        infos = socket.getaddrinfo(normalized, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError(f"hôte non résolu: {normalized}") from exc
    addresses = {info[4][0] for info in infos}
    if not addresses:
        raise ValueError(f"aucune adresse pour {normalized}")
    for raw in addresses:
        ip = ipaddress.ip_address(raw.split("%", 1)[0])
        if not ip.is_global:
            raise ValueError(f"cible réseau privée/réservée refusée: {normalized} -> {ip}")


def validate_http_url(url: str, allow_private_hosts: set[str]) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL non HTTP(S) refusée")
    if parsed.username or parsed.password:
        raise ValueError("userinfo dans URL refusé")
    if not parsed.hostname:
        raise ValueError("hôte manquant")
    resolve_public_host(parsed.hostname, allow_private_hosts)
    return parsed


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, allow_private_hosts: set[str]):
        super().__init__()
        self.allow_private_hosts = allow_private_hosts

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        validate_http_url(newurl, self.allow_private_hosts)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class BridgeServer(ThreadingHTTPServer):
    root: Path
    token: str
    allowed_origins: set[str]
    allow_private_hosts: set[str]
    max_batch_items: int
    max_bytes: int
    download_semaphore: threading.Semaphore
    event_log: Path


def download_item(server: BridgeServer, task_id: str, item: dict[str, Any]) -> None:
    with server.download_semaphore:
        url = str(item.get("url") or "")
        parsed = validate_http_url(url, server.allow_private_hosts)
        destination = safe_target(
            server.root / "mirror",
            str(item.get("subdir") or ""),
            str(item.get("filename") or Path(parsed.path).name or "artifact.bin"),
        )
        temp_path = destination.with_suffix(destination.suffix + ".part")
        expected_hash = str(item.get("sha256") or "").lower().strip()
        hasher = hashlib.sha256()
        downloaded = 0

        with TASK_LOCK:
            TASKS[task_id].update(status="downloading", bytes=0)

        opener = urllib.request.build_opener(SafeRedirectHandler(server.allow_private_hosts))
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with opener.open(request, timeout=60) as response, open(temp_path, "wb") as output:
                final_url = response.geturl()
                validate_http_url(final_url, server.allow_private_hosts)
                total = int(response.headers.get("Content-Length") or 0)
                if total and total > server.max_bytes:
                    raise ValueError(f"artefact trop volumineux: {total} > {server.max_bytes}")
                with TASK_LOCK:
                    TASKS[task_id]["total"] = total
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    downloaded += len(block)
                    if downloaded > server.max_bytes:
                        raise ValueError(f"limite de taille dépassée: {downloaded} > {server.max_bytes}")
                    output.write(block)
                    hasher.update(block)
                    with TASK_LOCK:
                        TASKS[task_id]["bytes"] = downloaded

            digest = hasher.hexdigest()
            if expected_hash and not secrets.compare_digest(digest, expected_hash):
                raise ValueError(f"SHA256 incorrect: {digest}")

            os.replace(temp_path, destination)
            result_manifest = {
                "task_id": task_id,
                "source_url": url,
                "filename": destination.name,
                "bytes": downloaded,
                "sha256": digest,
                "finished_at": time.time(),
            }
            atomic_json(server.root / "manifests" / f"download-{task_id}.json", result_manifest)
            append_event(server.event_log, {"type": "download.done", **result_manifest})
            with TASK_LOCK:
                TASKS[task_id].update(status="done", bytes=downloaded, sha256=digest, finished=time.time())
        except Exception as exc:
            temp_path.unlink(missing_ok=True)
            append_event(server.event_log, {"type": "download.error", "task_id": task_id, "error": str(exc)})
            with TASK_LOCK:
                TASKS[task_id].update(status="error", error=str(exc), finished=time.time())


def spawn_download(server: BridgeServer, item: dict[str, Any]) -> str:
    task_id = secrets.token_hex(8)
    with TASK_LOCK:
        TASKS[task_id] = {
            "id": task_id,
            "name": item.get("filename") or item.get("name"),
            "url": item.get("url"),
            "status": "queued",
            "created": time.time(),
        }
    threading.Thread(target=download_item, args=(server, task_id, item), daemon=True).start()
    return task_id


def count_json_files(path: Path) -> int:
    return sum(1 for _ in path.rglob("*.json")) if path.exists() else 0


class Handler(BaseHTTPRequestHandler):
    server: BridgeServer

    def log_message(self, *_args):
        return

    def origin(self) -> str | None:
        return self.headers.get("Origin")

    def cors(self) -> None:
        origin = self.origin()
        if origin and origin in self.server.allowed_origins:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-SIIAOS-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def respond(self, status: int, payload: Any) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def authorized(self) -> bool:
        supplied = self.headers.get("X-SIIAOS-Token", "")
        return bool(supplied) and secrets.compare_digest(supplied, self.server.token)

    def require_auth(self) -> bool:
        if self.authorized():
            return True
        self.respond(401, {"error": "token invalide"})
        return False

    def read_json(self, max_body: int = 2 * 1024 * 1024) -> Any:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > max_body:
            raise ValueError("taille de requête invalide")
        return json.loads(self.rfile.read(length))

    def do_OPTIONS(self):
        origin = self.origin()
        if origin and origin not in self.server.allowed_origins:
            self.respond(403, {"error": "origin non autorisée"})
            return
        self.send_response(204)
        self.cors()
        self.end_headers()

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/health":
            self.respond(200, {"ok": True, "bridge": "SIIAOS Local Bridge", "version": VERSION})
            return
        if not self.require_auth():
            return

        if path == "/tasks":
            with TASK_LOCK:
                tasks = list(TASKS.values())[-100:]
            self.respond(200, {"tasks": tasks})
            return

        if path == "/registry/summary":
            self.respond(
                200,
                {
                    "resources": count_json_files(self.server.root / "registry" / "resources"),
                    "approaches": count_json_files(self.server.root / "registry" / "approaches"),
                    "capabilities": count_json_files(self.server.root / "registry" / "capabilities"),
                    "signals": count_json_files(self.server.root / "signals"),
                    "observations": count_json_files(self.server.root / "observations"),
                    "benchmarks": count_json_files(self.server.root / "benchmarks"),
                    "evidence": count_json_files(self.server.root / "evidence"),
                    "gaps": count_json_files(self.server.root / "gaps"),
                },
            )
            return

        exports = {
            "/exports/radar-public": self.server.root / "projections" / "radar-public.json",
            "/exports/consultant-site": self.server.root / "projections" / "consultant-site.json",
        }
        if path in exports:
            export_path = exports[path]
            if not export_path.exists():
                self.respond(404, {"error": "projection absente"})
                return
            try:
                payload = json.loads(export_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                self.respond(500, {"error": "projection invalide"})
                return
            self.respond(200, payload)
            return

        self.respond(404, {"error": "not found"})

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if not self.require_auth():
            return
        try:
            payload = self.read_json()

            if path == "/batch":
                items = payload.get("items") if isinstance(payload, dict) else None
                if not isinstance(items, list) or not items:
                    raise ValueError("items requis")
                if len(items) > self.server.max_batch_items:
                    raise ValueError(f"batch trop grand: {len(items)} > {self.server.max_batch_items}")
                task_ids = [spawn_download(self.server, item) for item in items if isinstance(item, dict)]
                append_event(self.server.event_log, {"type": "batch.accepted", "count": len(task_ids), "task_ids": task_ids})
                self.respond(202, {"accepted": len(task_ids), "taskIds": task_ids})
                return

            if path == "/ingest/manifest":
                manifest_id = secrets.token_hex(10)
                envelope = {"id": manifest_id, "received_at": time.time(), "payload": payload}
                atomic_json(self.server.root / "inbox" / f"manifest-{manifest_id}.json", envelope)
                append_event(self.server.event_log, {"type": "manifest.ingested", "id": manifest_id})
                self.respond(202, {"accepted": True, "id": manifest_id})
                return

            if path == "/observations":
                if not isinstance(payload, dict):
                    raise ValueError("observation objet requise")
                if not payload.get("subject_id") or not payload.get("type"):
                    raise ValueError("subject_id et type requis")
                observation_id = secrets.token_hex(10)
                envelope = {"id": observation_id, "received_at": time.time(), **payload}
                atomic_json(self.server.root / "observations" / f"observation-{observation_id}.json", envelope)
                append_event(self.server.event_log, {"type": "observation.ingested", "id": observation_id, "subject_id": payload.get("subject_id")})
                self.respond(202, {"accepted": True, "id": observation_id})
                return

            self.respond(404, {"error": "not found"})
        except (ValueError, json.JSONDecodeError) as exc:
            self.respond(400, {"error": str(exc)})
        except Exception as exc:  # defensive boundary around localhost service
            append_event(self.server.event_log, {"type": "bridge.error", "error": str(exc), "path": path})
            self.respond(500, {"error": "erreur interne du bridge"})


def parse_origins(values: list[str]) -> set[str]:
    defaults = {
        "https://siiaos-resource-radar.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    }
    return defaults | {value.rstrip("/") for value in values if value.strip()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.home() / "SIIAOS-Radar-Core"))
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--token", default="")
    parser.add_argument("--max-batch-items", type=int, default=50)
    parser.add_argument("--max-mib", type=int, default=20 * 1024, help="Maximum MiB per downloaded artifact")
    parser.add_argument("--max-concurrency", type=int, default=3)
    parser.add_argument("--allow-origin", action="append", default=[])
    parser.add_argument("--allow-private-download-host", action="append", default=[])
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    for relative in (
        "mirror",
        "registry/resources",
        "registry/approaches",
        "registry/capabilities",
        "signals",
        "observations",
        "benchmarks",
        "evidence",
        "decisions",
        "gaps",
        "projections",
        "manifests",
        "inbox",
        "reports",
        "logs",
    ):
        (root / relative).mkdir(parents=True, exist_ok=True)

    token = args.token or secrets.token_urlsafe(24)
    server = BridgeServer(("127.0.0.1", args.port), Handler)
    server.root = root
    server.token = token
    server.allowed_origins = parse_origins(args.allow_origin)
    server.allow_private_hosts = {value.rstrip(".").lower() for value in args.allow_private_download_host}
    server.max_batch_items = max(1, min(args.max_batch_items, 200))
    server.max_bytes = max(1, args.max_mib) * 1024 * 1024
    server.download_semaphore = threading.Semaphore(max(1, min(args.max_concurrency, 16)))
    server.event_log = root / "logs" / "bridge-events.jsonl"

    print(f"SIIAOS Local Bridge V4 {VERSION} - http://127.0.0.1:{args.port}")
    print("Root:", root)
    print("Token:", token)
    print("Allowed origins:", ", ".join(sorted(server.allowed_origins)))
    print("Ctrl+C pour arrêter.")
    append_event(server.event_log, {"type": "bridge.started", "version": VERSION})
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        append_event(server.event_log, {"type": "bridge.stopped", "version": VERSION})
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
