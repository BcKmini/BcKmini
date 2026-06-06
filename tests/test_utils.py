"""Tests for generator/utils.py"""

import pytest
from generator.utils import (
    calculate_language_percentages,
    format_number,
    resolve_theme,
    get_language_color,
    esc,
    wrap_text,
)


def test_calculate_language_percentages_basic(sample_languages):
    result = calculate_language_percentages(sample_languages, ["HTML", "CSS", "Shell"], 8)
    names = [r["name"] for r in result]
    assert "Python" in names
    assert "HTML" not in names
    assert "CSS" not in names
    total = sum(r["percentage"] for r in result)
    assert 99.0 <= total <= 101.0


def test_calculate_language_percentages_max_display(sample_languages):
    result = calculate_language_percentages(sample_languages, [], 3)
    assert len(result) == 3
    assert result[0]["bytes"] >= result[1]["bytes"]


def test_calculate_language_percentages_empty():
    result = calculate_language_percentages({}, [], 8)
    assert result == []


def test_format_number():
    assert format_number(0) == "0"
    assert format_number(999) == "999"
    assert format_number(1000) == "1.0k"
    assert format_number(1500) == "1.5k"
    assert format_number(1_000_000) == "1.0M"
    assert format_number(2_500_000) == "2.5M"


def test_resolve_theme_defaults():
    theme = resolve_theme({})
    assert "void" in theme
    assert "synapse_cyan" in theme


def test_resolve_theme_override():
    custom = {"synapse_cyan": "#FF4500"}
    theme = resolve_theme(custom)
    assert theme["synapse_cyan"] == "#FF4500"
    assert "void" in theme  # defaults still present


def test_get_language_color_known():
    assert get_language_color("Python") == "#3572A5"
    assert get_language_color("TypeScript") == "#3178c6"


def test_get_language_color_unknown():
    color = get_language_color("SomeFutureLang")
    assert color.startswith("#")
    assert len(color) == 7


def test_esc_basic():
    assert esc("<script>") == "&lt;script&gt;"
    assert esc("AT&T") == "AT&amp;T"
    assert esc('say "hi"') == "say &quot;hi&quot;"


def test_wrap_text():
    lines = wrap_text("hello world foo bar", 10)
    for line in lines:
        assert len(line) <= 10 or " " not in line
