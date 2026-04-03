import os
from ai_job_market_analysis.utils import get_config

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")


def test_config_loads():
    config = get_config(CONFIG_PATH)
    assert isinstance(config, dict)


def test_config_has_dataset_key():
    config = get_config(CONFIG_PATH)
    assert "dataset" in config


def test_config_dataset_value():
    config = get_config(CONFIG_PATH)
    assert isinstance(config["dataset"], str)
    assert len(config["dataset"]) > 0
