import os
from pathlib import Path
from ..data.db import DB

def get_db_path():
    db_path_env = os.getenv("FOODKART_DB_DIR", "")
    if db_path_env:
        db_path = Path(db_path_env)
    else:
        db_path = Path.home() / "foodkart_db"
    return db_path

def get_db():
    db_path = get_db_path()
    return DB(db_path, "foodkart")