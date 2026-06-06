"""Tests for generator/cli_init.py"""

import pytest
from unittest.mock import patch
from generator.cli_init import DEFAULT_ARMS, COLORS


def test_default_arms_structure():
    assert len(DEFAULT_ARMS) >= 1
    for arm in DEFAULT_ARMS:
        assert "name" in arm
        assert "color" in arm
        assert "items" in arm


def test_colors_are_valid_theme_keys():
    valid_keys = {"synapse_cyan", "dendrite_violet", "axon_amber"}
    for color in COLORS:
        assert color in valid_keys
