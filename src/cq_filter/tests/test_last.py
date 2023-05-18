from cq_filter import Workplane


def test_last_rectangular_pockets(big_block_with_four_rectangular_pockets: Workplane):
    last = big_block_with_four_rectangular_pockets.last().objects
    assert len(last) == 4

    last_everything = big_block_with_four_rectangular_pockets.last(True).objects
    assert len(last_everything) == 20


def test_last_rectangular_holes(big_block_with_four_rectangular_holes: Workplane):
    last = big_block_with_four_rectangular_holes.last().objects
    assert len(last) == 0

    last_everything = big_block_with_four_rectangular_holes.last(True).objects
    assert len(last_everything) == 16


def test_last_circular_pockets(big_block_with_four_circular_pockets: Workplane):
    last = big_block_with_four_circular_pockets.last().objects
    assert len(last) == 4

    last_everything = big_block_with_four_circular_pockets.last(True).objects
    assert len(last_everything) == 8


def test_last_can_continue_extruding(big_block_with_four_rectangular_pockets):
    assert len(big_block_with_four_rectangular_pockets.faces().objects) == 26

    wp = (
        big_block_with_four_rectangular_pockets.last()
        .toWires()
        .toPending()
        .extrude(5)
        .faces()
    )

    assert len(wp.objects) == 6
