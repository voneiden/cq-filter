import pytest

from cq_filter import Workplane


@pytest.fixture
def wp() -> Workplane:
    return Workplane()


@pytest.fixture
def big_block(wp: Workplane) -> Workplane:
    return wp.rect(100, 100).extrude(10)


@pytest.fixture
def big_block_with_four_points(big_block: Workplane) -> Workplane:
    return (
        big_block.faces(">Z")
        .workplane()
        .pushPoints([(10, 10), (-15, -10), (0, 0), (13, -12)])
    )


@pytest.fixture
def big_block_with_four_rectangular_pockets(
    big_block_with_four_points: Workplane,
) -> Workplane:
    return big_block_with_four_points.rect(2, 2).cutBlind(-5)


@pytest.fixture
def big_block_with_four_rectangular_holes(
    big_block_with_four_points: Workplane,
) -> Workplane:
    return big_block_with_four_points.rect(2, 2).cutBlind(-10)


@pytest.fixture
def big_block_with_four_circular_pockets(
    big_block_with_four_points: Workplane,
) -> Workplane:
    return big_block_with_four_points.circle(2).cutBlind(-5)
