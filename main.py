#!/usr/bin/env python
"""bowling"""

from bowling import Game


def play_game():
    """play game"""
    game = Game()
    print("Game start")
    while game.frame_num != 10:
        game.roll(int(input("Roll for frame {}:".format(game.frame_num + 1))))

    bonus_round = 0
    if game.frames[9].check_strike:
        bonus_round = 2

    if game.frames[9].check_spare:
        bonus_round = 1

    for i in range(bonus_round):
        game.roll(int(input("Roll for bonus round {}:".format(i))))

    game.display_score_board()
    print("\ntotal score: ", game.score())


if __name__ == '__main__':
    play_game()
