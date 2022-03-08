"""CSC148 Assignment 1: Sample tests

=== CSC148 Winter 2022 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 0.

Warning: This is an extremely incomplete set of tests! Add your own tests
to be confident that your code is correct.

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) University of Toronto
"""
from datetime import date
from io import StringIO
from a1 import *

# A string representing a simple 4 by 4 game board.
# We use this in one of the tests below. You can use it in your own testing, but
# you do not have to.
SIMPLE_BOARD_STRING = 'P-B-\n-BRB\n--BB\n-C--'


def simple_board_setup() -> GameBoard:
    """Set up a simple game board"""
    b = GameBoard(4, 4)
    b.setup_from_grid(SIMPLE_BOARD_STRING)
    return b


def test_simple_place_character() -> None:
    """Test GameBoard.place_character by placing a single Raccoon."""
    b = GameBoard(3, 2)
    r = Raccoon(b, 1, 1)
    assert b.at(1, 1)[0] == r  # requires GameBoard.at be implemented to work


def test_simple_at() -> None:
    """Test GameBoard.at on docstring example"""
    b = GameBoard(3, 2)
    r = Raccoon(b, 1, 1)
    assert b.at(1, 1)[0] == r
    p = Player(b, 0, 1)
    assert b.at(0, 1)[0] == p


def test_simple_str() -> None:
    """Test GameBoard.__str__ for the simple board in SIMPLE_BOARD_STRING."""
    b = simple_board_setup()
    assert str(b) == 'P-B-\n-BRB\n--BB\n-C--'


def test_simple_check_game_end() -> None:
    """Test GameBoard.check_game_end on the docstring example"""
    b = GameBoard(3, 2)
    Raccoon(b, 1, 0)
    Player(b, 0, 0)
    RecyclingBin(b, 1, 1)
    assert b.check_game_end() is None
    assert not b.ended
    RecyclingBin(b, 2, 0)
    score = b.check_game_end()
    assert b.ended
    assert score == 11  # will only pass this last one when done Task 5.


def test_simple_adjacent_bin_score() -> None:
    """Test GameBoard.adjacent_bin_score on the docstring example"""
    b = GameBoard(3, 3)
    RecyclingBin(b, 1, 1)
    RecyclingBin(b, 0, 0)
    RecyclingBin(b, 2, 2)
    assert b.adjacent_bin_score() == 1
    RecyclingBin(b, 2, 1)
    assert b.adjacent_bin_score() == 3
    RecyclingBin(b, 0, 1)
    assert b.adjacent_bin_score() == 5


def test_simple_player_move() -> None:
    """Test Player.move on docstring example."""
    b = GameBoard(4, 2)
    p = Player(b, 0, 0)
    assert not p.move(UP)
    assert p.move(DOWN)
    assert b.at(0, 1) == [p]
    RecyclingBin(b, 1, 1)
    assert p.move(RIGHT)
    assert b.at(1, 1) == [p]


def test_simple_recyclingbin_move() -> None:
    """Test RecyclingBin.move on docstring example."""
    b = GameBoard(4, 2)
    rb = RecyclingBin(b, 0, 0)
    assert not rb.move(UP)
    assert rb.move(DOWN)
    assert b.at(0, 1) == [rb]


def test_simple_raccoon_check_trapped() -> None:
    """Test Raccoon.check_trapped on docstring example."""
    b = GameBoard(3, 3)
    r = Raccoon(b, 2, 1)
    Raccoon(b, 2, 2)
    Player(b, 2, 0)
    assert not r.check_trapped()
    RecyclingBin(b, 1, 1)
    assert r.check_trapped()


def test_simple_raccoon_move() -> None:
    """Test Raccoon.move on docstring example."""
    b = GameBoard(4, 2)
    r = Raccoon(b, 0, 0)
    assert not r.move(UP)
    assert r.move(DOWN)
    assert b.at(0, 1) == [r]
    g = GarbageCan(b, 1, 1, True)
    assert r.move(RIGHT)
    assert (r.x, r.y) == (0, 1)  # Raccoon didn't change its position
    assert not g.locked  # Raccoon unlocked the garbage can!
    assert r.move(RIGHT)
    assert r.inside_can
    assert len(b.at(1, 1)) == 2  # Raccoon and GarbageCan are both at (1, 1)!


def test_simple_raccoon_take_turn() -> None:
    """Test Raccoon.take_turn on docstring example."""
    b = GameBoard(3, 4)
    r1 = Raccoon(b, 0, 0)
    r1.take_turn()
    assert (r1.x, r1.y) in [(0, 1), (1, 0)]
    r2 = Raccoon(b, 2, 1)
    RecyclingBin(b, 2, 0)
    RecyclingBin(b, 1, 1)
    RecyclingBin(b, 2, 2)
    r2.take_turn()  # Raccoon is trapped
    assert (r2.x, r2.y) == (2, 1)


def test_simple_smartraccoon_take_turn() -> None:
    """Test SmartRaccoon.take_turn on docstring example."""
    b = GameBoard(8, 1)
    s = SmartRaccoon(b, 4, 0)
    GarbageCan(b, 3, 1, False)
    GarbageCan(b, 0, 0, False)
    GarbageCan(b, 7, 0, False)
    s.take_turn()
    assert s.x == 5
    s.take_turn()
    assert s.x == 6


def test_simple_give_turns() -> None:
    """Test GameBoard.give_turns on docstring example."""
    b = GameBoard(4, 3)
    p = Player(b, 0, 0)
    r = Raccoon(b, 1, 1)
    for _ in range(RACCOON_TURN_FREQUENCY - 1):
        b.give_turns()
    assert b.turns == RACCOON_TURN_FREQUENCY - 1
    assert (r.x, r.y) == (1, 1)  # Raccoon hasn't had a turn yet
    assert (p.x, p.y) == (0, 0)  # Player hasn't had any inputs
    p.record_event(RIGHT)
    b.give_turns()
    assert (r.x, r.y) != (1, 1)  # Raccoon has had a turn!
    assert (p.x, p.y) == (1, 0)  # Player moved right!

# ====== CUSTOM TESTS =========


def test_place_character_00() -> None:
    """Basic functionality"""
    b = GameBoard(10, 10)
    c1 = Player(b, 3, 3)
    c2 = Raccoon(b, 3, 4)
    c3 = GarbageCan(b, 3, 5, True)
    c4 = GarbageCan(b, 3, 6, False)
    c5 = SmartRaccoon(b, 3, 6)
    assert b.at(3, 3)[0] == c1
    assert b.at(3, 4)[0] == c2
    assert b.at(3, 5)[0] == c3
    assert b.at(3, 6)[0] == c4
    assert b.at(3, 6)[1] == c5
    assert len(b.at(3, 3)) == 1
    assert len(b.at(3, 5)) == 1
    assert len(b.at(3, 6)) == 2


def test_at_00() -> None:
    """1 character
    """
    b = GameBoard(10, 10)
    p = Player(b, 5, 5)
    assert b.at(5, 5)[0] == p
    assert len(b.at(5, 5)) == 1


def test_at_01() -> None:
    """2 characters r / gc
    """
    b = GameBoard(2, 2)
    g = GarbageCan(b, 0, 1, False)
    r = Raccoon(b, 0, 1)
    assert b.at(0, 1)[0] == g
    assert b.at(0, 1)[1] == r
    assert len(b.at(0, 1)) == 2


def test_at_02() -> None:
    """ sr / gc and off-board cases
    """
    b = GameBoard(2, 2)
    g = GarbageCan(b, 0, 1, False)
    r = SmartRaccoon(b, 0, 1)
    assert b.at(0, 1)[0] == g
    assert b.at(0, 1)[1] == r
    assert len(b.at(0, 1)) == 2
    assert b.at(2, 2) == []
    assert b.at(-1, -1) == []


def test_to_grid_00() -> None:
    """Basic Functionality and placing Raccoon in GC"""
    b = GameBoard(3, 3)
    _ = Player(b, 0, 0)
    _ = RecyclingBin(b, 0, 1)
    _ = SmartRaccoon(b, 0, 2)
    _ = GarbageCan(b, 1, 0, True)
    _ = GarbageCan(b, 1, 1, False)
    _ = RecyclingBin(b, 1, 2)
    _ = GarbageCan(b, 2, 0, False)
    _ = Raccoon(b, 2, 0)
    _ = RecyclingBin(b, 2, 1)
    _ = SmartRaccoon(b, 2, 2)
    # sry initialized this annoyingly it's going L→R one column at a time

    assert b.to_grid() == [['P', 'C', '@'], ['B', 'O', 'B'], ['S', 'B', 'S']]
    _ = Raccoon(b, 1, 1)
    assert b.to_grid() == [['P', 'C', '@'], ['B', '@', 'B'], ['S', 'B', 'S']]


def test_str_00() -> None:
    b = GameBoard(3, 3)
    _ = Player(b, 0, 0)
    _ = RecyclingBin(b, 0, 1)
    _ = SmartRaccoon(b, 0, 2)
    _ = GarbageCan(b, 1, 0, True)
    _ = GarbageCan(b, 1, 1, False)
    _ = RecyclingBin(b, 1, 2)
    _ = GarbageCan(b, 2, 0, False)
    _ = Raccoon(b, 2, 0)
    _ = RecyclingBin(b, 2, 1)
    _ = SmartRaccoon(b, 2, 2)
    assert b.__str__() == 'PC@\nBOB\nSBS'
    _ = SmartRaccoon(b, 1, 1)
    assert b.__str__() == 'PC@\nB@B\nSBS'


def test_check_trapped_00() -> None:
    b = GameBoard(1, 1)
    r = Raccoon(b, 0, 0)
    assert r.check_trapped()


def test_check_trapped_01() -> None:
    b = GameBoard(2, 2)
    r = Raccoon(b, 0, 1)
    assert not r.check_trapped()


def test_check_trapped_02() -> None:
    b = GameBoard(1, 7)
    r = Raccoon(b, 0, 3)
    assert not r.check_trapped()


def test_check_trapped_03() -> None:
    b = GameBoard(1, 7)
    r = Raccoon(b, 0, 3)
    _ = Player(b, 0, 4)
    _ = Player(b, 0, 2)
    assert r.check_trapped()


def test_check_trapped_04() -> None:
    b = GameBoard(9, 9)
    r = Raccoon(b, 5, 5)
    _ = RecyclingBin(b, 4, 5)
    _ = RecyclingBin(b, 6, 5)
    _ = RecyclingBin(b, 5, 4)
    _ = RecyclingBin(b, 5, 6)
    assert r.check_trapped() is True


def test_check_trapped_05() -> None:
    b = GameBoard(9, 9)
    r = Raccoon(b, 5, 5)
    _ = RecyclingBin(b, 4, 5)
    _ = RecyclingBin(b, 6, 5)
    _ = RecyclingBin(b, 5, 4)
    _ = GarbageCan(b, 5, 6, False)
    assert r.check_trapped()


def test_adjacent_bin_score_with_trapped_raccooon() -> None:
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


if __name__ == '__main__':
    import pytest

    pytest.main(['a1_sample_test.py'])
