"""Tests for the self-hosted contribution activity graph template."""

from generator.templates.activity_graph import generate as activity_graph_generate


def test_activity_graph_returns_svg(sample_config, sample_calendar):
    svg = activity_graph_generate(sample_config, sample_calendar)
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_activity_graph_shows_total(sample_config, sample_calendar):
    svg = activity_graph_generate(sample_config, sample_calendar)
    total = sum(d["count"] for d in sample_calendar)
    assert f"Total: {total}" in svg


def test_activity_graph_shows_date_range(sample_config, sample_calendar):
    svg = activity_graph_generate(sample_config, sample_calendar)
    assert sample_calendar[0]["date"] in svg
    assert sample_calendar[-1]["date"] in svg


def test_activity_graph_empty_calendar(sample_config):
    svg = activity_graph_generate(sample_config, [])
    assert "<svg" in svg
    assert "아직 수집된 데이터가 없습니다" in svg


def test_activity_graph_single_day(sample_config):
    svg = activity_graph_generate(sample_config, [{"date": "2026-01-01", "count": 3}])
    assert "<svg" in svg
    assert "2026-01-01" in svg


def test_activity_graph_all_zero_counts(sample_config):
    calendar = [{"date": f"2026-01-{d:02d}", "count": 0} for d in range(1, 6)]
    svg = activity_graph_generate(sample_config, calendar)
    assert "<svg" in svg
    assert "Total: 0" in svg


def test_activity_graph_custom_theme(sample_config, sample_calendar):
    config = {**sample_config, "theme": {"void": "#000000", "synapse_cyan": "#FF4500"}}
    svg = activity_graph_generate(config, sample_calendar)
    assert "#FF4500" in svg
