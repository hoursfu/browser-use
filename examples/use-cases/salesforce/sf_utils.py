"""
Shared utilities for Salesforce examples

What this file does:
- Provides helper functions to ensure Google Chrome is running with a remote debugging port, detect its PID, and construct a BrowserSession.
- Exposes a simple async prompt that waits for the user to press Enter before proceeding with automation.

How it fits into browser-use:
- Centralizes repeated setup logic used across Salesforce example scripts to keep them concise and consistent.

Notes:
- Defaults assume macOS with Google Chrome installed at the standard path.
- If PID detection fails, we still connect via CDP URL http://127.0.0.1:9222.
"""

# @file purpose: Helper utilities for Salesforce example scripts (Chrome debug + session + prompt).

from __future__ import annotations

import asyncio
import socket
import subprocess
import time
from typing import Optional, Tuple

from browser_use.browser import BrowserSession, BrowserProfile


def is_port_open(host: str, port: int, timeout: float = 0.25) -> bool:
    try:
        with socket.create_connection((host, port), timeout):
            return True
    except OSError:
        return False


def pid_listening_on_port(port: int) -> Optional[int]:
    """Return a PID listening on the given TCP port (macOS via lsof); None if not found."""
    try:
        proc = subprocess.run(
            ["lsof", f"-iTCP:{port}", "-sTCP:LISTEN", "-n", "-P"],
            capture_output=True,
            text=True,
            check=False,
        )
        lines = [l for l in proc.stdout.splitlines() if l.strip()]
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 2 and parts[1].isdigit():
                return int(parts[1])
    except Exception:
        return None
    return None


def ensure_debug_chrome(
    port: int = 9222,
    executable_path: str = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    user_data_dir: str = "/tmp/chrome-debug",
) -> Optional[int]:
    """Ensure Chrome is running with remote debugging on the specified port. Return PID if known, else None."""
    if is_port_open("127.0.0.1", port):
        return pid_listening_on_port(port)

    proc = subprocess.Popen([executable_path, f"--remote-debugging-port={port}", f"--user-data-dir={user_data_dir}"])

    # Wait up to ~10s for the port to open
    for _ in range(50):
        if is_port_open("127.0.0.1", port):
            break
        time.sleep(0.2)

    return proc.pid if is_port_open("127.0.0.1", port) else None


def ensure_debug_chrome_and_session(port: int = 9222) -> Tuple[Optional[int], BrowserSession]:
    """Launch Chrome if needed and return (pid, BrowserSession) connected to it.

    If PID cannot be determined, we still return a BrowserSession that connects via CDP URL.
    """
    pid = ensure_debug_chrome(port=port)
    if pid:
        return pid, BrowserSession(browser_pid=pid, browser_profile=BrowserProfile(highlight_elements=False))
    return None, BrowserSession(cdp_url=f"http://127.0.0.1:{port}", browser_profile=BrowserProfile(highlight_elements=False))


async def prompt_to_continue(message: str = "Chrome ready. Press Enter to start the agent...") -> None:
    try:
        await asyncio.to_thread(input, message)
    except Exception:
        # Non-interactive envs can safely ignore
        return


