"""test bowling"""

import unittest
from unittest import TestCase

from bowling import Frame, Game


class TestFrame(TestCase):
    """Frame Test"""

    def setUp(self) -> None:
        self.frame = Frame(1)


class TestFrameIsDone(TestFrame):
    """is_done tests"""

    def test_is_done_on_empty(self):
        """is_done on empty"""
        self.assertFalse(self.frame.is_done)

    def test_is_done_on_incomplete_frame(self):
        """test_is_done_on_incomplete_frame"""
        self.frame.throws.append(6)
        self.assertFalse(self.frame.is_done)

    def test_is_done_on_strike(self):
        """test_is_done_on_strike"""
        self.frame.throws.append(10)
        self.assertTrue(self.frame.is_done)

    def test_is_done_on_open_frame(self):
        """test_is_done_on_open_frame"""
        self.frame.throws.append(3)
        self.frame.throws.append(5)
        self.assertTrue(self.frame.is_done)


class TestFrameStrike(TestFrame):
    """check strike tests"""

    def test_check_strike_on_empty(self):
        """test_check_strike_on_empty"""
        self.assertFalse(self.frame.check_strike)

    def test_check_strike(self):
        """test_check_strike"""
        self.frame.throws.append(10)
        self.assertTrue(self.frame.check_strike)

    def test_check_strike_on_open_frame(self):
        """test_check_strike_on_open_frame"""
        self.frame.throws.append(3)
        self.frame.throws.append(5)
        self.assertFalse(self.frame.check_strike)

    def test_check_strike_on_spare(self):
        """test_check_strike_on_spare"""
        self.frame.throws.append(5)
        self.frame.throws.append(5)
        self.assertFalse(self.frame.check_strike)


class TestFrameSpare(TestFrame):
    """check spare tests"""

    def test_check_spare_on_empty(self):
        """test_check_spare_on_empty"""
        self.assertFalse(self.frame.check_spare)

    def test_check_spare(self):
        """test_check_spare"""
        self.frame.throws.append(3)
        self.frame.throws.append(7)
        self.assertTrue(self.frame.check_spare)

    def test_check_spare_on_open_frame(self):
        """test_check_spare_on_open_frame"""
        self.frame.throws.append(3)
        self.frame.throws.append(5)
        self.assertFalse(self.frame.check_spare)

    def test_check_spare_on_strike(self):
        """test_check_spare_on_strike"""
        self.frame.throws.append(10)
        self.assertFalse(self.frame.check_spare)


class TestFrameScore(TestFrame):
    """score tests"""

    def test_score_open_frame(self):
        """test_score_open_frame"""
        self.frame.throws.append(2)
        self.frame.throws.append(2)
        self.assertEqual(self.frame.score(None), 4)

    def test_score_strike(self):
        """test_score_strike"""
        self.frame.throws.append(10)
        self.assertEqual(self.frame.score([5, 5]), 20)

    def test_score_spare(self):
        """test_score_spare"""
        self.frame.throws.append(3)
        self.frame.throws.append(7)
        self.assertEqual(self.frame.score([5]), 15)


class TestFrameRoll(TestFrame):
    """Roll tests"""

    def test_roll_negative_pins(self):
        """test_roll_negative_pins"""
        with self.assertRaises(ValueError):
            self.frame.roll(-1)

    def test_roll_invalid_pins(self):
        """test_roll_invalid_pins"""
        with self.assertRaises(ValueError):
            self.frame.roll(11)

    def test_roll_invalid_roll_pins(self):
        """test_roll_invalid_roll_pins"""
        with self.assertRaises(ValueError):
            self.frame.roll(5)
            self.frame.roll(8)

    def test_roll_invalid_roll_count(self):
        """test_roll_invalid_roll_count"""
        with self.assertRaises(ValueError):
            self.frame.roll(5)
            self.frame.roll(3)
            self.frame.roll(2)

    def test_roll(self):
        """test_roll"""
        self.frame.roll(5)
        self.frame.roll(5)
        self.assertEqual(sum(self.frame.throws), 10)


class TestGame(TestCase):
    """Game basic tests"""

    def setUp(self) -> None:
        self.game = Game()


class TestGameGetFrame(TestGame):
    """get frame tests"""

    def test_get_frame(self):
        """test_get_frame"""
        frame = self.game.get_frame(5)
        self.assertEqual(frame.num, 6)

    def test_current_frame(self):
        """test_current_frame"""
        self.assertEqual(self.game.current_frame.num, 1)


class TestGameNextThrows(TestGame):
    """next throws tests"""

    def test_next_throws(self):
        """test_next_throws"""
        self.game.frames[8].throws = [5, 3]
        self.game.frames[9].throws = [5, 2]
        self.assertEqual(self.game.next_throws(8), [5, 2])


class TestGameHandleBonusThrow(TestGame):
    """bonus throw tests"""

    def test_handle_bonus_throw_not_a_strike_or_spare(self):
        """test_handle_bonus_throw_not_a_strike_or_spare"""
        self.game.frames[9].throws = [5, 2]
        with self.assertRaises(ValueError):
            self.game.handle_bonus_throw(5)

    def test_handle_bonus_throw_on_spare(self):
        """test_handle_bonus_throw_on_spare"""
        self.game.frames[9].throws = [5, 5]
        self.game.handle_bonus_throw(5)

    def test_handle_bonus_throw_on_spare_multiple_attempt(self):
        """test_handle_bonus_throw_on_spare_multiple_attempt"""
        self.game.frames[9].throws = [5, 5]
        self.game.handle_bonus_throw(5)
        with self.assertRaises(ValueError):
            self.game.handle_bonus_throw(5)

    def test_handle_bonus_throw_on_strike_multiple_attempt(self):
        """test_handle_bonus_throw_on_strike_multiple_attempt"""
        self.game.frames[9].throws = [10]
        self.game.handle_bonus_throw(5)
        self.game.handle_bonus_throw(5)
        with self.assertRaises(ValueError):
            self.game.handle_bonus_throw(5)

    def test_handle_bonus_throw_on_strike_invalid_pins(self):
        """test_handle_bonus_throw_on_strike_invalid_pins"""
        self.game.frames[9].throws = [10]
        self.game.handle_bonus_throw(5)
        with self.assertRaises(ValueError):
            self.game.handle_bonus_throw(7)

    def test_handle_bonus_throw_with_multiple_strike(self):
        """test_handle_bonus_throw_with_multiple_strike"""
        self.game.frames[9].throws = [10]
        self.game.handle_bonus_throw(10)
        self.game.handle_bonus_throw(10)


class TestGameRoll(TestGame):
    """game roll tests"""

    def test_roll(self):
        """test_roll"""
        self.game.roll(5)

    def test_roll_and_move_next(self):
        """test_roll_and_move_next"""
        self.game.roll(5)
        self.game.roll(5)

    def test_roll_and_10th_frame(self):
        """test_roll_and_10th_frame"""
        self.game.frame_num = 10
        self.game.frames[9].throws = [10]
        self.game.roll(5)
        self.game.roll(5)


class TestGameScore(TestGame):
    """game score tests"""

    def test_score_incomplete_game(self):
        """test_score_incomplete_game"""
        with self.assertRaises(IndexError):
            self.game.score()

    def test_score_10th_frame_spare_bonus_pending(self):
        """test_score_10th_frame_spare_bonus_pending"""
        self.game.frame_num = 10
        self.game.frames[9].throws = [5, 5]
        with self.assertRaises(IndexError):
            self.game.score()

    def test_score_10th_frame_strike_bonus_pending(self):
        """test_score_10th_frame_strike_bonus_pending"""
        self.game.frame_num = 10
        self.game.frames[9].throws = [10]
        with self.assertRaises(IndexError):
            self.game.score()

    def test_score(self):
        """test_score"""
        self.game.frame_num = 10
        self.game.frames[9].throws = [4, 4]
        self.game.score()

    def test_display_score_board(self):
        """test_display_score_board"""
        self.game.frame_num = 10
        self.game.frames[9].throws = [10]
        self.game.bonus_throws = [1, 2]
        self.game.display_score_board()


if __name__ == '__main__':
    unittest.main()
