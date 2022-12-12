#!/usr/bin/env python

import json
from pathlib import Path


def load_config_file(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


if Path("credentials.json").is_file():
    credentials = load_config_file("credentials.json")
elif Path(__file__).parent.joinpath("credentials.json").is_file():
    credentials = load_config_file(
        Path(__file__).parent.joinpath("credentials.json")
    )
elif Path("credentials.example.json").is_file():
    credentials = load_config_file("credentials.example.json")
else:
    credentials = load_config_file(
        Path(__file__).parent.joinpath("credentials.example.json")
    )
if Path("settings.json").is_file():
    settings = load_config_file("settings.json")
else:
    settings = load_config_file(
        Path(__file__).parent.joinpath("settings.json")
    )
