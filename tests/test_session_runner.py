"""Tests for DesktopSessionRunner unprivileged session management."""
import json
import os
from pathlib import Path
import subprocess
from unittest.mock import MagicMock

import pytest

from uhome_server.services.session_runner import (
    DesktopSessionRunner,
    DisplayEnvironmentError,
    DuplicateSessionError,
)


def test_command_vector_generation():
    runner = DesktopSessionRunner()
    steam_cmd = runner.build_command_vector("steam-console")
    assert steam_cmd == ["steam", "-tenfoot"]

    steam_extra = runner.build_command_vector("steam-console", ["-gamepadui"])
    assert steam_extra == ["steam", "-tenfoot", "-gamepadui"]

    thin_cmd = runner.build_command_vector("thin-gui")
    assert thin_cmd == ["python3", "-m", "uhome_server.thin_pages"]

    with pytest.raises(ValueError, match="Unknown presentation type"):
        runner.build_command_vector("unsupported")


def test_display_environment_check(monkeypatch):
    runner = DesktopSessionRunner()

    # Neither set
    monkeypatch.delenv("DISPLAY", raising=False)
    monkeypatch.delenv("WAYLAND_DISPLAY", raising=False)
    with pytest.raises(DisplayEnvironmentError):
        runner.check_display_environment(require_display=True)

    status = runner.check_display_environment(require_display=False)
    assert status["has_display"] is False
    assert status["session_type"] == "headless"

    # X11 display set
    monkeypatch.setenv("DISPLAY", ":0")
    status_x11 = runner.check_display_environment(require_display=True)
    assert status_x11["has_display"] is True
    assert status_x11["session_type"] == "x11"

    # Wayland display set
    monkeypatch.setenv("WAYLAND_DISPLAY", "wayland-0")
    status_wayland = runner.check_display_environment(require_display=True)
    assert status_wayland["has_display"] is True
    assert status_wayland["session_type"] == "wayland"


def test_session_lifecycle_with_mock_process(tmp_path: Path):
    mock_proc = MagicMock()
    mock_proc.pid = 4242
    mock_proc.wait.return_value = 0

    mock_spawner = MagicMock(return_value=mock_proc)
    runner = DesktopSessionRunner(
        state_dir=tmp_path / "sessions",
        process_spawner=mock_spawner,
        is_alive_checker=lambda pid: pid == 4242,
    )

    assert runner.current_focus == "uhome-console"
    assert runner.active_session is None

    # 1. Launch session
    handle = runner.launch_session("steam-console")
    assert handle.pid == 4242
    assert handle.presentation_type == "steam-console"
    assert runner.current_focus == "steam-console"

    # Spawner called without shell
    mock_spawner.assert_called_once()
    call_args, call_kwargs = mock_spawner.call_args
    assert call_args[0] == ["steam", "-tenfoot"]
    assert call_kwargs.get("shell") is False
    assert call_kwargs["env"]["HOMENEST_PRESENTATION"] == "steam-console"

    # 2. Prevent duplicate concurrent session
    with pytest.raises(DuplicateSessionError):
        runner.launch_session("thin-gui")

    # 3. Terminate session restores focus to console
    # Monkeypatch os.kill so we don't kill a real process
    terminated = runner.terminate_session()
    assert terminated["status"] == "terminated"
    assert terminated["focus"] == "uhome-console"
    assert runner.current_focus == "uhome-console"

    # 4. Verify telemetry events log
    log_file = tmp_path / "sessions" / "session_events.jsonl"
    assert log_file.exists()
    events = [json.loads(line) for line in log_file.read_text(encoding="utf-8").splitlines() if line]
    event_names = [e["event"] for e in events]
    assert "session_started" in event_names
    assert "session_terminated" in event_names
    assert "focus_restored" in event_names


def test_dead_pid_detection_restores_focus(tmp_path: Path):
    mock_proc = MagicMock()
    mock_proc.pid = 99999999  # Non-existent PID

    runner = DesktopSessionRunner(state_dir=tmp_path / "sessions", process_spawner=lambda *a, **kw: mock_proc)
    runner.launch_session("steam-console")

    # Active session should notice dead PID on check and restore focus
    session = runner.active_session
    assert session.status == "exited"
    assert runner.current_focus == "uhome-console"
