import os
from pathlib import Path

def get_db_path():
    db_path_env = os.getenv("FOODKART_DB_DIR", "")
    if db_path_env:
        db_path = Path(db_path_env)
    else:
        db_path = Path.home() / "foodkart_db"
    return db_path