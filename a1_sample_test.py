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


# My Test cases ================================================================
def test_place_multiple_characters() -> None:
    b = GameBoard(3, 3)
    r = Raccoon(b, 1, 1)
    p = Player(b, 0, 0)
    assert b.at(1, 1)[0] == r
    assert b.at(0, 0)[0] == p


def test_place_characters_on_same_spot() -> None:
    b = GameBoard(3, 3)
    r = Raccoon(b, 0, 0)
    p = Player(b, 0, 0)
    assert b.at(0, 0)[0] == r


def test_place_characters_raccoon_on_open_garbage_can() -> None:
    b = GameBoard(3, 3)
    o = GarbageCan(b, 1, 1, False)
    assert b.at(1, 1)[0] == o
    r = Raccoon(b, 1, 1)
    assert b.at(1, 1)[1] == r


def test_place_characters_raccoon_on_locked_garbage_can() -> None:
    b = GameBoard(3, 3)
    o = GarbageCan(b, 1, 1, True)
    assert b.at(1, 1)[0] == o
    r = Raccoon(b, 1, 1)
    assert b.at(1, 1) == [o]


def test_place_characters_raccoon_on_open_garbage_can_with_raccoon_in() -> None:
    b = GameBoard(3, 3)
    o = GarbageCan(b, 1, 1, False)
    assert b.at(1, 1)[0] == o
    r = Raccoon(b, 1, 1)
    assert b.at(1, 1) == [o, r]
    r2 = Raccoon(b, 1, 1)
    assert b.at(1, 1) == [o, r]


def test_place_characters_player_on_open_garbage_can() -> None:
    b = GameBoard(3, 3)
    o = GarbageCan(b, 1, 1, False)
    assert b.at(1, 1)[0] == o
    p = Player(b, 1, 1)
    assert b.at(1, 1) == [o]


# Task 2
def test_player_move_occupied_by_raccoon() -> None:
    b = GameBoard(4, 2)
    p = Player(b, 0, 0)
    r = Raccoon(b, 0, 1)
    assert p.move(DOWN) is False
    assert b.at(0, 1) == [r]
    assert b.at(0, 0) == [p]


def test_player_move_to_locked_garbage_can() -> None:
    b = GameBoard(4, 2)
    p = Player(b, 0, 0)
    c = GarbageCan(b, 1, 0, True)
    assert p.move(RIGHT) is False
    assert b.at(1, 0) == [c]
    assert b.at(0, 0) == [p]


def test_player_move_beyond_boundaries() -> None:
    b = GameBoard(4, 2)
    p = Player(b, 0, 0)
    p2 = Player(b, 3, 1)
    assert p.move(UP) is False
    assert p.move(LEFT) is False
    assert p2.move(DOWN) is False
    assert p2.move(RIGHT) is False


def test_player_move_to_moveable_recyclinbin() -> None:
    b = GameBoard(4, 2)
    p = Player(b, 0, 0)
    rb = RecyclingBin(b, 1, 1)

    assert p.move(DOWN) is True
    assert b.at(0, 1) == [p]

    assert p.move(RIGHT) is True
    assert b.at(1, 1) == [p]
    assert b.at(2, 1) == [rb]


def test_player_move_to_not_moveable_recyclinbin() -> None:
    b = GameBoard(4, 1)
    p = Player(b, 0, 0)
    rb = RecyclingBin(b, 1, 0)

    assert p.move(RIGHT) is True
    assert b.at(1, 0) == [p]
    assert b.at(2, 0) == [rb]

    assert p.move(RIGHT) is True
    assert b.at(2, 0) == [p]
    assert b.at(3, 0) == [rb]

    assert p.move(RIGHT) is False
    assert b.at(2, 0) == [p]
    assert b.at(3, 0) == [rb]


def test_player_move_multiple_recyclinbin() -> None:
    b = GameBoard(6, 1)
    p = Player(b, 0, 0)
    rb = RecyclingBin(b, 1, 0)
    rb2 = RecyclingBin(b, 3, 0)

    assert p.move(RIGHT) is True
    assert b.at(1, 0) == [p]
    assert b.at(2, 0) == [rb]
    assert b.at(3, 0) == [rb2]

    assert p.move(RIGHT) is True
    assert b.at(2, 0) == [p]
    assert b.at(3, 0) == [rb]
    assert b.at(4, 0) == [rb2]

    assert p.move(RIGHT) is True
    assert b.at(3, 0) == [p]
    assert b.at(4, 0) == [rb]
    assert b.at(5, 0) == [rb2]

    assert p.move(RIGHT) is False
    assert b.at(3, 0) == [p]
    assert b.at(4, 0) == [rb]
    assert b.at(5, 0) == [rb2]


def test_player_move_recyclinbin_then_blocked_by_garbage_can() -> None:
    b = GameBoard(6, 1)
    p = Player(b, 0, 0)
    rb = RecyclingBin(b, 1, 0)
    rb2 = RecyclingBin(b, 3, 0)
    o = GarbageCan(b, 5, 0, False)

    assert p.move(RIGHT) is True
    assert b.at(1, 0) == [p]
    assert b.at(2, 0) == [rb]
    assert b.at(3, 0) == [rb2]

    assert p.move(RIGHT) is True
    assert b.at(2, 0) == [p]
    assert b.at(3, 0) == [rb]
    assert b.at(4, 0) == [rb2]

    assert p.move(RIGHT) is False
    assert b.at(2, 0) == [p]
    assert b.at(3, 0) == [rb]
    assert b.at(4, 0) == [rb2]
    assert b.at(5, 0) == [o]


def test_player_move_recyclinbin_then_blocked_by_raccoon() -> None:
    b = GameBoard(6, 1)
    p = Player(b, 0, 0)
    rb = RecyclingBin(b, 1, 0)
    rb2 = RecyclingBin(b, 3, 0)
    r = Raccoon(b, 5, 0)

    assert p.move(RIGHT) is True
    assert b.at(1, 0) == [p]
    assert b.at(2, 0) == [rb]
    assert b.at(3, 0) == [rb2]

    assert p.move(RIGHT) is True
    assert b.at(2, 0) == [p]
    assert b.at(3, 0) == [rb]
    assert b.at(4, 0) == [rb2]

    assert p.move(RIGHT) is False
    assert b.at(2, 0) == [p]
    assert b.at(3, 0) == [rb]
    assert b.at(4, 0) == [rb2]
    assert b.at(5, 0) == [r]


def test_player_move_multiple_connected_and_disconnected_recyclinbin() -> None:
    b = GameBoard(4, 5)
    p = Player(b, 0, 0)
    rb1 = RecyclingBin(b, 1, 1)
    rb2 = RecyclingBin(b, 1, 3)
    rb3 = RecyclingBin(b, 2, 3)

    assert p.move(RIGHT) is True
    assert p.move(DOWN) is True
    assert b.at(1, 1) == [p]
    assert b.at(1, 2) == [rb1]

    assert p.move(DOWN) is True
    assert b.at(1, 2) == [p]
    assert b.at(1, 3) == [rb1]
    assert b.at(1, 4) == [rb2]

    assert p.move(LEFT) is True
    assert p.move(DOWN) is True

    assert p.move(RIGHT) is True
    assert b.at(1, 3) == [p]
    assert b.at(2, 3) == [rb1]
    assert b.at(1, 4) == [rb2]
    assert b.at(3, 3) == [rb3]

    assert p.move(RIGHT) is False


def test_player_move_to_not_empty_unlocked_garbage_can() -> None:
    b = GameBoard(6, 1)
    p = Player(b, 0, 0)
    rb = RecyclingBin(b, 1, 0)
    rb2 = RecyclingBin(b, 3, 0)
    c = GarbageCan(b, 5, 0, True)

    assert p.move(RIGHT) is True
    assert b.at(1, 0) == [p]
    assert b.at(2, 0) == [rb]
    assert b.at(3, 0) == [rb2]

    assert p.move(RIGHT) is True
    assert b.at(2, 0) == [p]
    assert b.at(3, 0) == [rb]
    assert b.at(4, 0) == [rb2]

    assert p.move(RIGHT) is False
    assert b.at(2, 0) == [p]
    assert b.at(3, 0) == [rb]
    assert b.at(4, 0) == [rb2]
    assert b.at(5, 0) == [c]





# My Test cases ================================================================



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


if __name__ == '__main__':
    import pytest

    pytest.main(['a1_sample_test.py'])
