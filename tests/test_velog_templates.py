"""Tests for the Velog SVG templates."""

from generator.templates.velog_summary import generate as velog_summary_generate
from generator.templates.velog_ranking import generate as velog_ranking_generate
from generator.templates.velog_trend import generate as velog_trend_generate


def test_velog_summary_returns_svg(sample_config, sample_velog_stats):
    svg = velog_summary_generate(sample_config, sample_velog_stats)
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_velog_summary_contains_values(sample_config, sample_velog_stats):
    svg = velog_summary_generate(sample_config, sample_velog_stats)
    assert "12.3k" in svg  # format_number(12345)
    assert "testvelog" in svg


def test_velog_summary_handles_zero_diff(sample_config, sample_velog_stats):
    stats = {**sample_velog_stats, "post_diff": 0}
    svg = velog_summary_generate(sample_config, stats)
    assert "– 0" in svg


def test_velog_ranking_returns_svg(sample_config, sample_velog_stats):
    svg = velog_ranking_generate(sample_config, sample_velog_stats["top_posts"])
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_velog_ranking_contains_titles(sample_config, sample_velog_stats):
    svg = velog_ranking_generate(sample_config, sample_velog_stats["top_posts"])
    assert "가장 인기있는 글" in svg


def test_velog_ranking_empty_posts(sample_config):
    svg = velog_ranking_generate(sample_config, [])
    assert "<svg" in svg
    assert "데이터가 아직 없습니다" in svg


def test_velog_trend_returns_svg(sample_config, sample_velog_history):
    svg = velog_trend_generate(sample_config, sample_velog_history)
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_velog_trend_insufficient_history(sample_config):
    svg = velog_trend_generate(sample_config, [{"date": "2026-01-01", "total_views": 100}])
    assert "<svg" in svg
    assert "추이를 표시하려면" in svg
