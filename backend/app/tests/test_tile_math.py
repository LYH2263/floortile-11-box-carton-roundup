import pytest

from app.engines.tile_math import layout_preview, tile_count


def test_guest_room_600_waste8():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    assert r["area_m2"] == 27.0
    assert r["raw_count"] == 75
    assert r["order_count"] == 81
    assert r["layout"]["cols"] == 10
    assert r["layout"]["rows"] == 8
    assert r["layout"]["grid_count"] == 80


def test_layout_preview_small_room():
    lp = layout_preview(2.5, 2.0, 0.6, 0.6)
    assert lp["cols"] == 5
    assert lp["rows"] == 4
    assert lp["grid_count"] == 20


def test_zero_waste():
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0)
    assert r["raw_count"] == 9
    assert r["order_count"] == 9


def test_box_size_one_is_identity():
    # N=1 时进位后等于进位前
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, box_size=1)
    assert r["box_size"] == 1
    assert r["box_count"] == r["order_count"] == 81
    assert r["boxed_count"] == 81


def test_box_round_up_to_multiple():
    # order_count=81，N=4 → 81/4 向上取整 21 箱，21*4=84 片
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, box_size=4)
    assert r["order_count"] == 81
    assert r["box_count"] == 21
    assert r["boxed_count"] == 84


def test_box_exact_multiple_no_padding():
    # 已是整倍时不多补：order_count=9，N=3 → 3 箱 9 片
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0, box_size=3)
    assert r["order_count"] == 9
    assert r["box_count"] == 3
    assert r["boxed_count"] == 9


def test_box_size_zero_or_negative_rejected():
    for bad in (0, -1, -4):
        with pytest.raises(ValueError):
            tile_count(3.0, 3.0, 1.0, 1.0, 0.0, box_size=bad)
