import pytest
from os import path


@pytest.fixture
def root_directory():
    return path.dirname(path.abspath(__file__))
