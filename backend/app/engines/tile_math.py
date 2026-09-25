"""Floor tile order count: area method + optional grid layout preview."""

from app.engines.helpers import ceil_units


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
    box_size: int = 1,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    order_count: ceil(raw * (1 + waste_pct/100))  # 进位前面积法订货量
    box_count / boxed_count: order_count 向上取整到 box_size 整倍后的箱数与片数
    box_size=1 时进位后等于进位前；box_size<=0 非法。
    """
    if int(box_size) <= 0:
        raise ValueError("box_size must be positive")
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    with_waste = ceil_units(raw * (1 + float(waste_pct) / 100.0))
    box_n = int(box_size)
    box_count = ceil_units(with_waste / box_n)
    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "order_count": with_waste,
        "box_size": box_n,
        "box_count": box_count,
        "boxed_count": box_count * box_n,
        "layout": layout,
    }


def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    """Grid count if tiles are laid on a full rectangular lattice (may exceed area method)."""
    cols = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    grid_count = cols * rows
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": grid_count,
    }
