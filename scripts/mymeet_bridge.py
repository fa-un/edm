#!/usr/bin/env python3
"""Receive one raw MyMeet transcript over a short-lived localhost HTTP bridge.

The clipboard must be read by the browser-side CUA runtime. This process only
receives UTF-8 bytes, writes them atomically to a new Markdown file, and emits
metadata (never transcript contents).
"""

from __future__ import annotations

import argparse
import hashlib
import http.server
import json
import os
import secrets
import sys
import tempfile
import threading
from pathlib import Path
from urllib.parse import urlsplit

MAX_BODY_BYTES = 25 * 1024 * 1024
ALLOWED_ORIGINS = {"https://app.mymeet.ai"}


class BridgeServer(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def __init__(self, address: tuple[str, int], handler: type[http.server.BaseHTTPRequestHandler], output: Path, token: str, max_bytes: int) -> None:
        super().__init__(address, handler)
        self.output = output
        self.token = token
        self.max_bytes = max_bytes
        self.received = threading.Event()
        self.result: dict[str, object] | None = None


class Handler(http.server.BaseHTTPRequestHandler):
    server: BridgeServer

    def log_message(self, _format: str, *_args: object) -> None:
        # The URL includes a one-time bearer token. Never write request lines.
        return

    def _cors(self) -> None:
        origin = self.headers.get("Origin")
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Bridge-Token")

    def _respond(self, status: int, body: dict[str, object]) -> None:
        encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def do_OPTIONS(self) -> None:  # noqa: N802
        origin = self.headers.get("Origin")
        if origin not in ALLOWED_ORIGINS:
            self._respond(403, {"ok": False, "error": "origin_not_allowed"})
            return
        self.send_response(204)
        self._cors()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        if self.server.received.is_set():
            self._respond(410, {"ok": False, "error": "bridge_already_used"})
            return
        parsed = urlsplit(self.path)
        expected_path = "/receive/" + self.server.token
        if parsed.path != expected_path:
            self._respond(404, {"ok": False, "error": "not_found"})
            return
        origin = self.headers.get("Origin")
        if origin is not None and origin not in ALLOWED_ORIGINS:
            self._respond(403, {"ok": False, "error": "origin_not_allowed"})
            return
        media_type = self.headers.get_content_type().lower()
        if media_type != "text/plain":
            self._respond(415, {"ok": False, "error": "expected_text_plain"})
            return
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            self._respond(400, {"ok": False, "error": "invalid_content_length"})
            return
        if length <= 0:
            self._respond(400, {"ok": False, "error": "empty_body"})
            return
        if length > self.server.max_bytes:
            self._respond(413, {"ok": False, "error": "body_too_large"})
            return

        payload = self.rfile.read(length)
        if len(payload) != length:
            self._respond(400, {"ok": False, "error": "incomplete_body"})
            return
        try:
            payload.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            self._respond(400, {"ok": False, "error": "invalid_utf8"})
            return

        temporary: str | None = None
        try:
            self.server.output.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary = tempfile.mkstemp(prefix=".mymeet-", suffix=".tmp", dir=self.server.output.parent)
            with os.fdopen(fd, "wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            saved = Path(temporary)
            verify = saved.read_bytes()
            if verify != payload:
                raise OSError("round_trip_mismatch")
            # Hard-link creation is atomic and fails if the destination exists.
            os.link(saved, self.server.output)
            saved.unlink()
            temporary = None
        except FileExistsError:
            if temporary:
                Path(temporary).unlink(missing_ok=True)
            self._respond(409, {"ok": False, "error": "destination_exists"})
            return
        except OSError:
            if temporary:
                Path(temporary).unlink(missing_ok=True)
            self._respond(500, {"ok": False, "error": "write_failed"})
            return
        finally:
            if temporary:
                Path(temporary).unlink(missing_ok=True)

        digest = hashlib.sha256(payload).hexdigest()
        self.server.result = {
            "ok": True,
            "path": str(self.server.output),
            "bytes": len(payload),
            "sha256": digest,
        }
        self.server.received.set()
        self._respond(200, self.server.result)


def receive(args: argparse.Namespace) -> int:
    output = Path(args.output).expanduser().resolve()
    if output.suffix.lower() != ".md":
        print("ERROR: output path must end in .md", file=sys.stderr)
        return 2
    if output.exists():
        print("ERROR: output path already exists", file=sys.stderr)
        return 2
    if args.timeout <= 0:
        print("ERROR: timeout must be positive", file=sys.stderr)
        return 2

    token = secrets.token_urlsafe(24)
    server = BridgeServer(("127.0.0.1", 0), Handler, output, token, args.max_bytes)
    server.timeout = min(args.timeout, 1)
    host, port = server.server_address
    print(json.dumps({"ready": True, "url": f"http://{host}:{port}/receive/{token}", "timeout_seconds": args.timeout}, ensure_ascii=False), flush=True)

    deadline = threading.Event()
    timer = threading.Timer(args.timeout, deadline.set)
    timer.daemon = True
    timer.start()
    try:
        while not server.received.is_set() and not deadline.is_set():
            server.handle_request()
        if server.result is None:
            print(json.dumps({"ok": False, "error": "timeout"}), flush=True)
            return 1
        print(json.dumps(server.result, ensure_ascii=False), flush=True)
        return 0
    finally:
        timer.cancel()
        server.server_close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    receiver = subparsers.add_parser("receive", help="receive one UTF-8 transcript from the browser CUA runtime")
    receiver.add_argument("--output", required=True, help="absolute or relative destination .md path; must not exist")
    receiver.add_argument("--timeout", type=int, default=120, help="seconds to wait for the one-time POST (default: 120)")
    receiver.add_argument("--max-bytes", type=int, default=MAX_BODY_BYTES, help="maximum payload size (default: 25 MiB)")
    receiver.set_defaults(func=receive)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.max_bytes <= 0:
        print("ERROR: max-bytes must be positive", file=sys.stderr)
        return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
