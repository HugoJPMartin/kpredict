import pytest
import json
import os
from kpredict import ConfigParser


@pytest.fixture
def config_1():
    return ConfigParser(os.path.join(os.path.dirname(__file__), "data", ".config_1"))

@pytest.fixture
def config_2():
    return ConfigParser(os.path.join(os.path.dirname(__file__), "data", ".config_2"))

@pytest.fixture
def config_3():
    return ConfigParser(os.path.join(os.path.dirname(__file__), "data", ".config_3"))

@pytest.fixture
def config_file():
    return os.path.join(os.path.dirname(__file__), "data", ".config_1")