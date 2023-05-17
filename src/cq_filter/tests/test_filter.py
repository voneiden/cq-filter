import pytest

from cq_filter.cq_filter import Cluster, Workplane


def test_inheritance():
    wp = Workplane()
    wp2 = wp.rect(2, 2).extrude(2)

    assert isinstance(wp, Workplane)
    assert isinstance(wp2, Workplane)
    assert hasattr(wp2, "filter")


@pytest.fixture
def wp_with_rects():
    wp = (
        Workplane()
        .pushPoints([(0, 10), (0, -10), (0, 20), (5, 15)])
        .rect(2, 2)
        .extrude(1)
        .faces(">Z")
    )
    return wp


def test_filter(wp_with_rects):
    filtered_objs = wp_with_rects.filter(
        lambda face: round(face.Center().y, 4) >= 15
    ).objects
    assert len(filtered_objs) == 2


def test_sort(wp_with_rects):
    sorted_y = wp_with_rects.sort(lambda o: o.Center().y)

    sorted_y_objs = sorted_y[0].objects
    assert len(sorted_y_objs) == 1
    assert sorted_y_objs[0].Center().y == -10
    sorted_y_objs = sorted_y[-1].objects
    assert sorted_y_objs[0].Center().y == 20

    sorted_x = sorted_y.sort(lambda o: o.Center().x)

    sorted_x_objs = sorted_x[0].objects
    assert len(sorted_x_objs) == 1
    assert round(sorted_x_objs[0].Center().x, 4) == 0
    sorted_x_objs = sorted_x[-1].objects
    assert round(sorted_x_objs[0].Center().x, 4) == 5


def test_group(wp_with_rects):
    grouped = wp_with_rects.group(Cluster(lambda o: o.Center().x))
    grouped_x_objs = grouped[0].objects
    assert len(grouped_x_objs) == 3

    grouped_x_objs = grouped[0:].objects
    assert len(grouped_x_objs) == 4
