def register_asset(db_path, name, asset_type):
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO assets (name, type) VALUES (?, ?)
    """, (name, asset_type))
    conn.commit()
    conn.close()
def register_version(db_path, asset_id, version_number, path, preview_path=None):
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO versions (asset_id, version_number, path, preview_path)
        VALUES (?, ?, ?, ?)
    """, (asset_id, version_number, path, preview_path))
    conn.commit()
    conn.close()
def search_assets(db_path, asset_type=None):
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM assets"
    if asset_type:
        query += " WHERE type = ?"
        cursor.execute(query, (asset_type,))
    else:
        cursor.execute(query)
    assets = cursor.fetchall()
    conn.close()
    return assets
