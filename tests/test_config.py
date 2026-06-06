"""Tests for generator/config.py"""

import pytest
import tempfile
import os
import yaml

from generator.config import load_config, validate_config, ConfigError


def _write_config(data: dict) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False, encoding="utf-8")
    yaml.dump(data, f)
    f.close()
    return f.name


def test_load_valid_config(sample_config):
    path = _write_config(sample_config)
    try:
        cfg = load_config(path)
        assert cfg["username"] == "testuser"
    finally:
        os.unlink(path)


def test_load_missing_file():
    with pytest.raises(ConfigError, match="not found"):
        load_config("/nonexistent/path/config.yml")


def test_validate_missing_username():
    cfg = {"profile": {"name": "Test"}}
    with pytest.raises(ConfigError, match="username"):
        validate_config(cfg)


def test_validate_galaxy_arms_type():
    cfg = {"username": "u", "galaxy_arms": "not_a_list"}
    with pytest.raises(ConfigError, match="galaxy_arms"):
        validate_config(cfg)


def test_validate_passes_minimal():
    cfg = {"username": "mini"}
    validate_config(cfg)  # should not raise


def test_load_applies_defaults(sample_config):
    path = _write_config({"username": "mini"})
    try:
        cfg = load_config(path)
        assert "theme" in cfg
        assert "languages" in cfg
    finally:
        os.unlink(path)
