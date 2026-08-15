"""Chrome Debug Bridge - runs on Windows, exposes CDP to WSL.

Raw TCP relay: WSL -> 0.0.0.0:9223 -> 127.0.0.1:9222 (Chrome DevTools).
Tunnels both plain HTTP (/json/*) and WebSocket (/devtools/*) transparently.
The Host header of the first request on each connection is rewritten to
localhost so Chrome's DevTools host check is satisfied.

Usage (PowerShell):
    python C:\\tools\\chrome-bridge.py              # launches Chrome with a debug profile, then bridges
    python C:\\tools\\chrome-bridge.py --no-launch  # Chrome already running with --remote-debugging-port
"""
import argparse
import os
import re
import socket
import subprocess
import sys
import threading
import time

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
PROFILE_DIR = "C:\\temp\\chrome-debug"

chrome_port = 9222


def log(msg: str) -> None:
    print(f"  [bridge] {msg}", flush=True)


def relay(src: socket.socket, dst: socket.socket) -> None:
    try:
        while True:
            data = src.recv(65536)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        for s in (src, dst):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass


def handle_client(client: socket.socket, addr: tuple) -> None:
    try:
        first = client.recv(65536)
        if not first:
            client.close()
            return
        first = re.sub(
            rb"(?im)^Host: [^\r\n]+",
            f"Host: localhost:{chrome_port}".encode(),
            first,
            count=1,
        )
        line = first.split(b"\r\n", 1)[0].decode(errors="replace")
        # Prefer IPv6 loopback: a stale `netsh portproxy 0.0.0.0:9222 -> 127.0.0.1:9222`
        # can shadow the IPv4 port and loop back on itself; Chrome still binds [::1].
        upstream = None
        for host in ("::1", "127.0.0.1"):
            try:
                upstream = socket.create_connection((host, chrome_port), timeout=10)
                break
            except OSError:
                continue
        if upstream is None:
            raise OSError(f"cannot reach Chrome on port {chrome_port}")
        upstream.settimeout(None)
        upstream.sendall(first)
        log(f"{addr[0]} {line}")
        t = threading.Thread(target=relay, args=(upstream, client), daemon=True)
        t.start()
        relay(client, upstream)
        t.join()
    except Exception as e:  # noqa: BLE001
        log(f"error: {e}")
    finally:
        try:
            client.close()
        except OSError:
            pass


def launch_chrome(port: int) -> subprocess.Popen | None:
    if not os.path.exists(CHROME_PATH):
        log(f"Chrome not found at {CHROME_PATH}")
        return None
    log(f"Launching Chrome (debug port {port}, profile {PROFILE_DIR})")
    return subprocess.Popen([
        CHROME_PATH,
        f"--remote-debugging-port={port}",
        "--remote-allow-origins=*",
        f"--user-data-dir={PROFILE_DIR}",
    ])


def main() -> None:
    global chrome_port
    parser = argparse.ArgumentParser(description="Chrome Debug Bridge for WSL")
    parser.add_argument("--chrome-port", type=int, default=9222)
    parser.add_argument("--bridge-port", type=int, default=9223)
    parser.add_argument("--no-launch", action="store_true")
    args = parser.parse_args()
    chrome_port = args.chrome_port

    if not args.no_launch:
        chrome = launch_chrome(args.chrome_port)
        if chrome:
            time.sleep(2)
            log(f"Chrome PID: {chrome.pid}")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", args.bridge_port))
    srv.listen(16)
    log(f"Listening 0.0.0.0:{args.bridge_port} -> localhost:{args.chrome_port}")
    log("Ctrl+C to stop\n")
    try:
        while True:
            c, a = srv.accept()
            threading.Thread(target=handle_client, args=(c, a), daemon=True).start()
    except KeyboardInterrupt:
        log("Shutting down")
    finally:
        srv.close()


if __name__ == "__main__":
    main()
