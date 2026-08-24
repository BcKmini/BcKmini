"""Tests for the local Velog history JSON store."""

import json

from generator.velog_history import diff_from_days_ago, load_history, update_history


def test_update_history_creates_file(tmp_path, sample_velog_stats):
    path = str(tmp_path / "data" / "velog_history.json")
    history = update_history(path, sample_velog_stats, today="2026-01-15")

    assert len(history) == 1
    assert history[0]["date"] == "2026-01-15"
    assert history[0]["total_views"] == sample_velog_stats["total_views"]

    with open(path, "r", encoding="utf-8") as f:
        assert json.load(f) == history


def test_update_history_overwrites_same_day(tmp_path, sample_velog_stats):
    path = str(tmp_path / "velog_history.json")
    update_history(path, sample_velog_stats, today="2026-01-15")

    updated_stats = {**sample_velog_stats, "total_views": 99999}
    history = update_history(path, updated_stats, today="2026-01-15")

    assert len(history) == 1
    assert history[0]["total_views"] == 99999


def test_update_history_appends_new_day(tmp_path, sample_velog_stats):
    path = str(tmp_path / "velog_history.json")
    update_history(path, sample_velog_stats, today="2026-01-14")
    history = update_history(path, sample_velog_stats, today="2026-01-15")

    assert [h["date"] for h in history] == ["2026-01-14", "2026-01-15"]


def test_load_history_missing_file_returns_empty(tmp_path):
    path = str(tmp_path / "does_not_exist.json")
    assert load_history(path) == []


def test_diff_from_days_ago(sample_velog_history):
    diff = diff_from_days_ago(sample_velog_history, 7, "total_views")
    assert diff == sample_velog_history[-1]["total_views"] - sample_velog_history[0]["total_views"]


def test_diff_from_days_ago_insufficient_history():
    assert diff_from_days_ago([{"date": "2026-01-01", "total_views": 100}], 7, "total_views") == 0


def test_diff_from_days_ago_empty_history():
    assert diff_from_days_ago([], 7, "total_views") == 0
