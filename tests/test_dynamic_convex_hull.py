from app.dynamic_convex_hull import DynamicConvexHull
from app.point import Point

def simple_points():
    return [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]

def test_insert_and_query():
    dch = DynamicConvexHull()
    pts = simple_points()
    for p in pts:
        dch.insert(p)
    for p in pts:
        assert dch.is_inside(p)
    assert not dch.is_inside(Point(2, 2))
    assert dch.is_inside(Point(0.5, 0.5))

def test_delete_one_point():
    dch = DynamicConvexHull()
    pts = simple_points()
    for p in pts:
        dch.insert(p)
    dch.delete(pts[0])
    assert not dch.is_inside(pts[0])
    for p in pts[1:]:
        assert dch.is_inside(p)
    assert dch.is_inside(Point(0.5, 0.5))

def test_delete_all_points():
    dch = DynamicConvexHull()
    pts = simple_points()
    for p in pts:
        dch.insert(p)
    for p in pts:
        dch.delete(p)
    hull = dch.get_hull()
    assert len(hull) == 0 or all(not dch.is_inside(Point(x, y)) for x in range(3) for y in range(3))

def test_delete_non_existent_point():
    dch = DynamicConvexHull()
    pts = simple_points()
    for p in pts:
        dch.insert(p)
    result = dch.delete(Point(100, 100))
    assert result is False
    assert all(dch.is_inside(p) for p in pts)

def test_double_delete():
    dch = DynamicConvexHull()
    pts = simple_points()
    for p in pts:
        dch.insert(p)
    dch.delete(pts[0])
    result = dch.delete(pts[0])
    assert result is False
    assert not dch.is_inside(pts[0])

def test_delete_and_reinsert():
    dch = DynamicConvexHull()
    pts = simple_points()
    for p in pts:
        dch.insert(p)
    dch.delete(pts[0])
    dch.insert(pts[0])
    assert dch.is_inside(pts[0])

def test_complex_insert_delete_mix():
    dch = DynamicConvexHull()
    pts = [Point(x, 0) for x in range(10)]
    for p in pts:
        dch.insert(p)
    for i in [3, 5, 7]:
        dch.delete(pts[i])
    for i, p in enumerate(pts):
        if i in [3, 5, 7]:
            assert not dch.is_inside(p)
        else:
            assert dch.is_inside(p)
    if len(pts) - 3 >= 3:
        assert dch.is_inside(Point(5, 0))

def test_multiple_structures_merge_and_delete():
    dch = DynamicConvexHull()
    pts = [Point(x, 0) for x in range(8)] + [Point(0, y) for y in range(8)]
    for p in pts:
        dch.insert(p)
    for p in pts[:5]:
        dch.delete(p)
    for i, p in enumerate(pts):
        if i < 5:
            assert not dch.is_inside(p)
        else:
            assert dch.is_inside(p)

