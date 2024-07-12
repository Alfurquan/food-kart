import tinydb

class DB:
    def __init__(self, db_path: str, table_name: str, db_file_prefix: str):
        self.db = tinydb.TinyDB(
            db_path / f"{db_file_prefix}.json", create_dirs=True
        )
        self.table_name = table_name
        
    def create(self, item: dict):
        id = self.get_table().insert(item)
        return id
    
    def update(self, id: int, mods: dict):
        changes = {k: v for k, v in mods.items() if v is not None}
        self.get_table().update(changes, doc_ids=[id])
    
    def get_table(self):
        return self.db.table(self.table_name)
    
    def get_item_by_id(self, id: int):
        return self.get_table().get(doc_id=id)
    
    def get_all(self):
        return self.get_table().all()
    
    def close(self):
        self.db.close()