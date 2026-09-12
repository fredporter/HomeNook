"""Tests for HomeNest standalone lifecycle, decoupling from HA, and state compliance."""
import os
from pathlib import Path
import pytest

from uhome_server.config import get_homenest_state_dir
from uhome_server.services.playback_service import PlaybackService
from uhome_server.services.uhome_presentation_service import UHomePresentationService


def test_presentation_lifecycle_honest_observation(tmp_path, monkeypatch):
    monkeypatch.setenv("UDOS_HOME", str(tmp_path / "udos_home"))
    service = UHomePresentationService(repo_root=tmp_path / "repo")

    # 1. Initially idle
    status = service.get_status()
    assert status["active_presentation"] is None
    assert status["running"] is False
    assert status["lifecycle_state"] == "idle"
    assert status["focus"] == "console"

    # 2. Starting without a live process tracks launching intent, NOT false running health
    service.start("steam-console")
    status = service.get_status()
    assert status["active_presentation"] == "steam-console"
    assert status["running"] is False
    assert status["lifecycle_state"] == "launching"

    # 3. Starting with current process PID observes active process
    my_pid = os.getpid()
    service.start("steam-console", pid=my_pid)
    status = service.get_status()
    assert status["active_presentation"] == "steam-console"
    assert status["running"] is True
    assert status["lifecycle_state"] == "running"
    assert status["focus"] == "steam-console"

    # 4. Dead PID detection: an impossible PID (e.g. 99999999) must be observed as exited
    service.start("steam-console", pid=99999999)
    status = service.get_status()
    assert status["running"] is False
    assert status["lifecycle_state"] == "exited"
    assert status["focus"] == "console"

    # 5. Stop restores focus to console and resets to idle
    service.stop()
    status = service.get_status()
    assert status["active_presentation"] is None
    assert status["running"] is False
    assert status["lifecycle_state"] == "idle"


def test_playback_handoff_honest_status(tmp_path, monkeypatch):
    monkeypatch.setenv("UDOS_HOME", str(tmp_path / "udos_home"))
    service = PlaybackService(repo_root=tmp_path / "repo")

    result = service.handoff("sample-movie-456", target_client="living-room-tv")
    assert result["success"] is True
    assert result["status"] == "queued"
    assert result["acknowledged"] is False
    assert result["item_id"] == "sample-movie-456"

    queue = service.get_queue()
    assert len(queue) == 1
    assert queue[0]["item_id"] == "sample-movie-456"

    service.clear_queue()
    assert len(service.get_queue()) == 0


def test_state_directory_under_udos_home(tmp_path, monkeypatch):
    udos_home = tmp_path / "custom_udos_home"
    monkeypatch.setenv("UDOS_HOME", str(udos_home))
    repo_root = tmp_path / "custom_repo"
    repo_root.mkdir()

    pres_svc = UHomePresentationService(repo_root=repo_root)
    pres_svc.start("thin-gui")

    play_svc = PlaybackService(repo_root=repo_root)
    play_svc.handoff("sample-track")

    # State must be under UDOS_HOME/homenest
    assert (udos_home / "homenest" / "presentation" / "presentation.json").exists()
    assert (udos_home / "homenest" / "playback" / "playback_queue.json").exists()

    # Must NOT have created legacy repo memory
    assert not (repo_root / "memory").exists()
