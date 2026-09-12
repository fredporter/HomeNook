"""Unprivileged desktop session runner for HomeNest presentations."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import signal
import subprocess
from typing import Any, Callable
import uuid

from uhome_server.config import get_homenest_state_dir, utc_now_iso_z


class SessionError(RuntimeError):
    pass


class DuplicateSessionError(SessionError):
    pass


class DisplayEnvironmentError(SessionError):
    pass


class SessionHandle:
    def __init__(
        self,
        session_id: str,
        presentation_type: str,
        pid: int,
        started_at: str,
        command: list[str],
        env: dict[str, str],
        process: subprocess.Popen | None = None,
    ):
        self.session_id = session_id
        self.presentation_type = presentation_type
        self.pid = pid
        self.started_at = started_at
        self.command = command
        self.env = env
        self.process = process
        self.status = "running"
        self.exit_code: int | None = None
        self.terminated_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "presentation_type": self.presentation_type,
            "pid": self.pid,
            "started_at": self.started_at,
            "command": self.command,
            "status": self.status,
            "exit_code": self.exit_code,
            "terminated_at": self.terminated_at,
        }


class DesktopSessionRunner:
    """Manages the launch, tracking, termination, and focus restoration of unprivileged desktop sessions."""

    def __init__(
        self,
        state_dir: Path | None = None,
        process_spawner: Callable[..., subprocess.Popen] | None = None,
        is_alive_checker: Callable[[int], bool] | None = None,
    ):
        self._custom_state_dir = state_dir
        self._active_session: SessionHandle | None = None
        self._process_spawner = process_spawner or subprocess.Popen
        self._is_alive_checker = is_alive_checker
        self._focus_target = "uhome-console"

    @property
    def state_dir(self) -> Path:
        return self._custom_state_dir or (get_homenest_state_dir() / "sessions")

    @property
    def current_focus(self) -> str:
        return self._focus_target

    @property
    def active_session(self) -> SessionHandle | None:
        if self._active_session and self._active_session.status == "running":
            # Refresh liveness
            if not self._is_alive(self._active_session.pid):
                self._active_session.status = "exited"
                self._active_session.terminated_at = utc_now_iso_z()
                self._restore_focus()
        return self._active_session

    def _is_alive(self, pid: int) -> bool:
        if self._is_alive_checker is not None:
            return self._is_alive_checker(pid)
        if pid <= 0:
            return False
        try:
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, PermissionError):
            return False

    def check_display_environment(self, require_display: bool = True) -> dict[str, Any]:
        """Check for active Wayland or X11 graphical display environment."""
        display = os.environ.get("DISPLAY")
        wayland_display = os.environ.get("WAYLAND_DISPLAY")
        has_display = bool(display or wayland_display)

        if require_display and not has_display:
            raise DisplayEnvironmentError(
                "No graphical environment detected (neither DISPLAY nor WAYLAND_DISPLAY set)"
            )

        return {
            "has_display": has_display,
            "display": display,
            "wayland_display": wayland_display,
            "session_type": "wayland" if wayland_display else ("x11" if display else "headless"),
        }

    def build_command_vector(
        self,
        presentation_type: str,
        extra_args: list[str] | None = None,
    ) -> list[str]:
        """Generate a safe, vector-based execution command without shell interpretation."""
        extra = extra_args or []
        if presentation_type == "steam-console":
            return ["steam", "-tenfoot"] + extra
        elif presentation_type == "thin-gui":
            return ["python3", "-m", "uhome_server.thin_pages"] + extra
        else:
            raise ValueError(f"Unknown presentation type: {presentation_type}")

    def _log_event(self, event_type: str, data: dict[str, Any]) -> None:
        try:
            target_dir = self.state_dir
            target_dir.mkdir(parents=True, exist_ok=True)
            log_file = target_dir / "session_events.jsonl"
            payload = {
                "event": event_type,
                "timestamp": utc_now_iso_z(),
                **data,
            }
            with log_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(payload) + "\n")
        except Exception:
            pass

    def launch_session(
        self,
        presentation_type: str,
        extra_args: list[str] | None = None,
        require_display: bool = False,
        env_overrides: dict[str, str] | None = None,
    ) -> SessionHandle:
        """Launch an unprivileged desktop session, preventing concurrent duplicates."""
        # 1. Check for active session
        if self.active_session is not None and self.active_session.status == "running":
            raise DuplicateSessionError(
                f"Session already running: {self.active_session.session_id} (pid={self.active_session.pid})"
            )

        # 2. Check display environment if requested
        self.check_display_environment(require_display=require_display)

        # 3. Generate safe command vector
        cmd = self.build_command_vector(presentation_type, extra_args)

        session_id = f"sess-{uuid.uuid4().hex[:8]}"
        started_at = utc_now_iso_z()

        # Build clean environment
        env = dict(os.environ)
        if env_overrides:
            env.update(env_overrides)
        env["HOMENEST_SESSION_ID"] = session_id
        env["HOMENEST_PRESENTATION"] = presentation_type

        # 4. Spawn process using non-shell vector
        proc = self._process_spawner(
            cmd,
            shell=False,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        handle = SessionHandle(
            session_id=session_id,
            presentation_type=presentation_type,
            pid=proc.pid,
            started_at=started_at,
            command=cmd,
            env=env_overrides or {},
            process=proc,
        )

        self._active_session = handle
        self._focus_target = presentation_type

        self._log_event("session_started", handle.to_dict())
        return handle

    def terminate_session(self, timeout_seconds: float = 2.0) -> dict[str, Any]:
        """Terminate the active session gracefully (SIGTERM -> SIGKILL) and restore focus."""
        session = self._active_session
        if not session or session.status != "running":
            self._restore_focus()
            return {"status": "no_active_session", "focus": self._focus_target}

        pid = session.pid
        exit_code = None

        if self._is_alive(pid):
            try:
                os.kill(pid, signal.SIGTERM)
                if session.process:
                    try:
                        exit_code = session.process.wait(timeout=timeout_seconds)
                    except subprocess.TimeoutExpired:
                        os.kill(pid, signal.SIGKILL)
                        exit_code = session.process.wait(timeout=1.0)
            except (ProcessLookupError, PermissionError):
                pass

        session.status = "stopped"
        session.exit_code = exit_code
        session.terminated_at = utc_now_iso_z()

        self._restore_focus()
        self._log_event("session_terminated", session.to_dict())

        return {
            "status": "terminated",
            "session_id": session.session_id,
            "exit_code": exit_code,
            "focus": self._focus_target,
        }

    def _restore_focus(self) -> None:
        """Reset window/input focus back to the primary console."""
        self._focus_target = "uhome-console"
        self._log_event("focus_restored", {"focus": self._focus_target})
