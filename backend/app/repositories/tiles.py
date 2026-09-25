from app.db import connect


def list_tiles():
    conn = connect()
    try:
        return [dict(r) for r in conn.execute("SELECT * FROM tiles ORDER BY id").fetchall()]
    finally:
        conn.close()


def get_tile(tile_id: int):
    conn = connect()
    try:
        row = conn.execute("SELECT * FROM tiles WHERE id=?", (tile_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_box_size(tile_id: int, box_size: int):
    """只改每箱片数 N；不影响任何已写入的测算记录。返回受影响行数。"""
    conn = connect()
    try:
        cur = conn.execute(
            "UPDATE tiles SET box_size=? WHERE id=?", (box_size, tile_id)
        )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()
