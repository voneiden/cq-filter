from pytest import approx

from cq_filter.cq_filter import Workplane


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


def test_sort_dist():
    wp = (
        Workplane()
        .rect(10, 10)
        .extrude(10)
        .faces(">Z")
        .workplane()
        .rect(5, 5)
        .cutBlind(-5)
        .faces("|Z")
    )

    assert len(wp.objects) == 3

    wp = wp.sort(dist="Z")

    assert wp.objects[0].Area() == approx(100)
    assert wp.objects[1].Area() == approx(25)
    assert wp.objects[2].Area() == approx(75)

    wp = wp.sort(dist="-Z")

    assert wp.objects[0].Area() == approx(75)
    assert wp.objects[1].Area() == approx(25)
    assert wp.objects[2].Area() == approx(100)
