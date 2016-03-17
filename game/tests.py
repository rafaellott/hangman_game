from django.test import TestCase
from service import HangmanGame
import unittest


class TestApp(unittest.TestCase):

    def setUp(self):
        self.game = HangmanGame()
        self.chosen_word = self.game.storage['word']

    def test_01__check_instance(self):
        self.assertIsInstance(
            self.game, HangmanGame, msg="Is not the same object"
        )

    def test_02__check_word_was_chosen(self):
        self.assertIsInstance(self.game.storage['word'], basestring)

    def test_03__check_wrong_tries(self):
        vocabulary = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for v in vocabulary:
            if v not in self.chosen_word:
                resp = self.game.check_letter(v)
                self.assertEquals(resp['wrong_tries'], 1)
                break

    def test_04__check_wrong_tries(self):
        vocabulary = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for v in vocabulary:
            if v not in self.chosen_word:
                resp = self.game.check_letter(v)
                self.assertEquals(resp['wrong_tries'], 1)
                break

    def test_05__check_right_tries(self):
        self.game.check_letter(self.chosen_word[0])
        self.assertEquals(self.storage['right_tries'], 1)

    def test_06__check_win(self):
        for l in self.chosen_word:
            self.game.check_letter(l)
            self.assertEquals(self.game.win(), 1)
