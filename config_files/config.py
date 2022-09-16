#!/usr/bin/env python

import json
from pathlib import Path


def load_config_file(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


if Path("config.json").is_file():
    config = load_config_file("config.json")
else:
    config = load_config_file(Path(__file__).parent.joinpath("config.json"))
