from fastapi import APIRouter, HTTPException

from app.repositories import tiles as tile_repo
from app.schemas.tile import TileBoxSizeUpdate

router = APIRouter(tags=["tiles"])


@router.get("/tiles")
def list_tiles():
    return {"items": tile_repo.list_tiles()}


@router.get("/tiles/{tile_id}")
def get_tile(tile_id: int):
    row = tile_repo.get_tile(tile_id)
    if not row:
        raise HTTPException(404, "tile not found")
    return row


@router.patch("/tiles/{tile_id}")
def update_tile(tile_id: int, body: TileBoxSizeUpdate):
    # 仅维护每箱片数 N；不触碰任何已落库测算单的进位结果
    if tile_repo.update_box_size(tile_id, body.box_size) == 0:
        raise HTTPException(404, "tile not found")
    return tile_repo.get_tile(tile_id)
