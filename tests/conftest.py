import pytest
from unittest.mock import Mock
from foodkart.data.db import DB


@pytest.fixture()
def db():
    return Mock(spec=DB)
    