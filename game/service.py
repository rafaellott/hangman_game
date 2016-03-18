from __future__ import unicode_literals
import random

WORDS = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
NUMCHANCE = 4


class HangmanGame(object):

    def __init__(self, storage=None):
        if not storage:
            # create a new game
            storage = dict(
                chosen_word=random.choice(WORDS),
                letter_used=[],
                wrong_tries=0,
                right_tries=0,
                msg_call='You have 5 tries remaining'
            )
            print storage['chosen_word']
        self.storage = storage

    def draw(self):
        return [
            '_ ' if i not in self.storage['letter_used'] else i
            for i in self.storage['chosen_word']
        ]

    def lost(self):
        return self.storage['wrong_tries'] > NUMCHANCE

    def win(self):
        return self.storage['right_tries'] == len(self.storage['chosen_word'])

    def state(self):
        resp = dict(
            letter_used=self.storage['letter_used'],
            wrong_tries=self.storage['wrong_tries'],
            winner=self.win(),
            lose=self.lost(),
            msg=self.storage['msg_call'],
            draw=self.draw()
        )
        if resp['winner']:
            resp['msg'] = 'Congratulations. You won!'
        if resp['lose']:
            resp['msg'] = 'Well, looks like you lost'
        return resp

    def check_letter(self, letter):
        # only one letter
        try:
            if self.win() or self.lost():
                raise Exception('end game')
            if (
                not letter or not isinstance(letter, basestring) or
                len(letter) != 1
            ):
                raise Exception('letter invalid')
            # check if the given letter has been chosen before
            if letter in self.storage['letter_used']:
                raise Exception('You already tryied "%s"' % letter.upper())
            self.storage['letter_used'].append(letter)
            # check if the given letter is in the chosen_word
            if letter in self.storage['chosen_word']:
                self.storage['right_tries'] += self.storage[
                    'chosen_word'].count(letter)
            else:
                self.storage['wrong_tries'] += 1
                raise Exception (
                    'you have %d tries remaining' %
                    (NUMCHANCE - self.storage['wrong_tries'] + 1)
                )
        except Exception as e:
            self.storage['msg_call'] = e.message
        return self.state()
