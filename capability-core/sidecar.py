#!/usr/bin/env python3
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import engine

HOST = os.environ.get("SIIAOS_CORE_BIND", "127.0.0.1")
PORT = int(os.environ.get("SIIAOS_CORE_PORT", "8765"))
TOKEN = os.environ.get("SIIAOS_CORE_TOKEN", "")

def is_loopback(host):
    if host in {"localhost", "127.0.0.1", "::1"}:
        return True
    try:
        return ip_address(host).is_loopback
    except ValueError:
        return False

if not is_loopback(HOST) and not TOKEN:
    raise SystemExit("Refusing non-loopback bind without SIIAOS_CORE_TOKEN")

class Handler(BaseHTTPRequestHandler):
    server_version = "SIIAOSCapabilityCore/0.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _authorized(self):
        if not TOKEN:
            return True
        value = self.headers.get("Authorization", "")
        return value == "Bearer " + TOKEN

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {
                "ok": True,
                "service": "siiaos-capability-core",
                "protocol_version": "0.1"
            })
            return
        self._send(404, {"error": "not_found"})

    def do_POST(self):
        if self.path != "/v0.1/execute":
            self._send(404, {"error": "not_found"})
            return
        if not self._authorized():
            self._send(401, {"error": "unauthorized"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 2_000_000:
                raise ValueError("invalid content length")
            payload = json.loads(self.rfile.read(length))
            if payload.get("protocol_version") != "0.1":
                self._send(400, {"error": "unsupported_protocol_version"})
                return
            result = engine.execute(payload)
            self._send(200, result)
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            self._send(400, {"error": "bad_request", "detail": str(exc)})
        except Exception as exc:
            self._send(500, {"error": "internal_error", "detail": type(exc).__name__})

def main():
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(json.dumps({
        "service": "siiaos-capability-core",
        "bind": HOST,
        "port": PORT,
        "protocol_version": "0.1",
        "auth": bool(TOKEN)
    }), flush=True)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
