from fastapi import HTTPException

from app.engines.tile_math import tile_count
from app.repositories import history, rooms, settings_repo, tiles


def run_estimate(room_id: int, tile_id: int, waste_pct: float | None, save: bool, note: str):
    room = rooms.get_room(room_id)
    if not room:
        raise HTTPException(404, "room not found")
    tile = tiles.get_tile(tile_id)
    if not tile:
        raise HTTPException(404, "tile not found")
    if room.get("data_quality") == "dirty":
        raise HTTPException(422, "room marked dirty; fix dimensions before estimate")

    # N 以砖型当前配置为准；落库时快照进 calc_runs，事后改砖型默认 N 不重算旧单
    box_size = tile.get("box_size")
    box_size = int(box_size) if box_size is not None else 1
    if box_size <= 0:
        raise HTTPException(422, "tile box_size must be positive")

    waste = float(waste_pct) if waste_pct is not None else settings_repo.get_waste_pct()
    calc = tile_count(
        room["length"], room["width"], tile["tile_l"], tile["tile_w"], waste, box_size
    )

    run_id = None
    if save:
        payload = {**calc, "room_id": room_id, "tile_id": tile_id}
        run_id = history.insert_run(room_id, tile_id, waste, payload, note, box_size)

    return {
        "room_id": room_id,
        "tile_id": tile_id,
        "room": room,
        "tile": tile,
        "run_id": run_id,
        **calc,
    }
