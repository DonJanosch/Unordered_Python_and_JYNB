#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      MacenkaJ
#
# Created:     06.11.2017
# Copyright:   (c) MacenkaJ 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import numpy as np

class player:
    def __init__(self, name):
        self.name = name
        self.x = -1
        self.y = -1
        self.valid_move = False
        self.turns = 0

    def getName(self):
        return self.name

    def increaseTurns(self):
        self.turns +=1

    def get_move_coordinates(self):
        return self.x, self.y

    def getMoves(self):
        return self.turns

    def choose_next_move(self):
        x,y = input('{}: please input coordinates for your next move (x,y)'.format(self.name)).split(',')
        self.x,self.y = int(x)-1, int(y)-1
        return self.x,self.y

    def toogle_valid_move(self):
        self.valid_move = not(self.valid_move)

class ttt_game:
    player_id_to_int = {0:1,1:-1}
    int_to_str = {1:'X',-1:'O'}

    def __init__(self,player_0,player_1):
        self.game_over = False
        self.field = np.zeros((3,3),dtype=np.int8)
        self.pretty_field = [(3,3)]
        self.turn = 0
        self.turns = 0
        self.x, self.y = 0, 0
        self.players = []
        self.players.append(player_0)
        self.players.append(player_1)

    def ask_for_move(self,playerId:int):
        self.players[playerId].choose_next_move()

    def check_move_validity(self):
        move_is_valid = False
        x_check, y_check = self.players[self.turn].get_move_coordinates()
        if x_check >= 0 and x_check <= 2 and y_check >= 0 and y_check <= 2:
            if self.field[x_check,y_check] == 0:
                move_is_valid = True
        if move_is_valid:
            print('Move from Player {} accepted!'.format(self.players[self.turn].getName()))
            self.players[self.turn].toogle_valid_move()
        else:
            print('This move is not possible, please give me a nother one!')

    def make_move(self):
        x_move, y_move = self.players[self.turn].get_move_coordinates()
        value_move = self.player_id_to_int[self.turn]
        self.field[x_move,y_move] = value_move
        self.toogle_turns()
        self.players[self.turn].increaseTurns()
        self.players[self.turn].toogle_valid_move()
        print(self.field)

    def toogle_turns(self):
        self.turn = abs(self.turn -1)

    def check_victory(self):
        for x in range(3):
            if np.abs(np.sum(self.field[:,x])) ==3 or np.abs(np.sum(self.field[x,:])) ==3:#check rows and columns
                self.game_over = True
                self.turn = abs(self.turn -1)
            if np.abs(self.field[0,0]+self.field[1,1]+self.field[2,2]) == 3 or np.abs(self.field[0,2]+self.field[1,1]+self.field[2,0]) == 3: #check diagonals
                self.game_over = True
                self.turn = abs(self.turn -1)

    def get_current_player_name(self):
        return self.players[self.turn].getName()

    def get_current_player_moves(self):
        return self.players[self.turn].getMoves()

def main():
    player_1 = player('Jan')
    player_2 = player('Sepp')
    my_game = ttt_game(player_1,player_2)
    print('Starting a new Game: {} vs {}'.format(my_game.players[0].getName(),my_game.players[1].getName()))
    print(my_game.field)
    while True:
        while not(my_game.players[my_game.turn].valid_move):
            my_game.ask_for_move(my_game.turn)
            my_game.check_move_validity()
        my_game.make_move()
        my_game.check_victory()

        if my_game.game_over == True:
            print('Game Over: {} has won after {} moves!'.format(my_game.get_current_player_name(),my_game.get_current_player_moves()))
            break

if __name__ == '__main__':
    main()
