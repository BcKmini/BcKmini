"""Tests for SVG generation templates."""

import pytest
from generator.templates.tech_stack import generate as tech_stack_generate
from generator.templates.stats_card import generate as stats_card_generate


def test_tech_stack_returns_svg(sample_config, sample_languages):
    svg = tech_stack_generate(sample_config, sample_languages)
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_tech_stack_contains_language_names(sample_config, sample_languages):
    svg = tech_stack_generate(sample_config, sample_languages)
    assert "Python" in svg
    assert "TypeScript" in svg


def test_tech_stack_excludes_filtered_languages(sample_config, sample_languages):
    svg = tech_stack_generate(sample_config, sample_languages)
    assert ">HTML<" not in svg
    assert ">CSS<" not in svg


def test_tech_stack_contains_sector_names(sample_config, sample_languages):
    svg = tech_stack_generate(sample_config, sample_languages)
    assert "AI Engineering" in svg
    assert "Web &amp; Backend" in svg or "Web & Backend" in svg


def test_tech_stack_empty_languages(sample_config):
    svg = tech_stack_generate(sample_config, {})
    assert "<svg" in svg
    assert "No language data" in svg


def test_stats_card_returns_svg(sample_config, sample_stats):
    svg = stats_card_generate(sample_config, sample_stats)
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_stats_card_contains_values(sample_config, sample_stats):
    svg = stats_card_generate(sample_config, sample_stats)
    assert "342" in svg
    assert "28" in svg


def test_tech_stack_custom_theme(sample_config, sample_languages):
    config = {**sample_config, "theme": {"void": "#000000", "synapse_cyan": "#FF4500"}}
    svg = tech_stack_generate(config, sample_languages)
    assert "#FF4500" in svg
