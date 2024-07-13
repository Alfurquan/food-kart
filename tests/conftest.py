import pytest
from foodkart.data.db import DB


@pytest.fixture(scope='session')
def tmp_db_path(tmp_path_factory):
    """
    Path to temporary database
    """
    return tmp_path_factory.mktemp("foodkart_db")

@pytest.fixture(scope='session')
def foodkart_db(tmp_db_path):
    """
    foodkart db
    """
    print(tmp_db_path)
    db = DB(tmp_db_path, "foodkart")
    yield db
    db.close()
    