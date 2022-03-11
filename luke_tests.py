from a1 import *


def test_adjacent_bin_score_with_trapped_raccoon() -> None:
    b = GameBoard(2, 2)
    _ = GarbageCan(b, 0, 0, False)
    r = Raccoon(b, 0, 0)

    # The raccoon was placed on a garbage can, it should reflect that
    assert r.inside_can == True
    assert b.adjacent_bin_score() == 0

    # The raccoon is in a bin, and there are no adjacent recycling bins
    assert b.check_game_end() == 0

    # We introduce two recycling bins, but they aren't adjacent
    _ = RecyclingBin(b, 0, 1)
    _ = RecyclingBin(b, 1, 0)

    assert b.adjacent_bin_score() == 1
    assert b.check_game_end() == 1

    # This is a connecting recycling bin, so the adjacent bin score is 3
    _ = RecyclingBin(b, 1, 1)

    assert b.adjacent_bin_score() == 3
    assert b.check_game_end() == 3


def test_adjacent_bin_score() -> None:
    b = GameBoard(3, 3)

    _ = RecyclingBin(b, 0, 1)
    _ = RecyclingBin(b, 1, 0)

    # A single bin is a "cluster"
    assert b.adjacent_bin_score() == 1

    _ = RecyclingBin(b, 0, 0)

    assert b.adjacent_bin_score() == 3


def test_adjacent_bin_score_loop() -> None:
    b = GameBoard(3, 3)
    b.setup_from_grid("BBB\nB-B\nBBB")

    assert b.at(1, 1) == []
    assert b.adjacent_bin_score() == 8

    b.setup_from_grid("BBB\nBBB\nBBB")

    assert b.adjacent_bin_score() == 9


def test_adjacent_bin_score_multiple_groups() -> None:
    b = GameBoard(5, 4)
    b.setup_from_grid("BB---\nBB--B\n---BB\n--BB")

    assert b.adjacent_bin_score() == 5


def test_smart_raccoon_movement() -> None:
    b = GameBoard(5, 1)
    b.setup_from_grid("O-----O")

    s = SmartRaccoon(b, 3, 0)
    s.take_turn()

    # Should go to the left as that's the order given in DIRECTIONS
    assert s.x == 2

    s.x = 4
    s.take_turn()

    # Should go to the right regardless of DIRECTIONS because its closer
    assert s.x == 5

def test_adjacent_hang() -> None:
    b = GameBoard(5, 5)
    b.setup_from_grid("B----\nBB----\nB")

    assert b.adjacent_bin_score() == 4

if __name__ == "__main__":
    import pytest  # type: ignore

    pytest.main(["luke_tests.py"])
