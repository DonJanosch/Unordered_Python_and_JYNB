import numpy as np

class player:
    def __init__(self, name):
        self.name = name
        self.x = -1
        self.y = -1
        self.valid_move = False
        self.turns = 0
        self.wins = 0
        self.input_neurons = 9
        self.hidden_neurons = 60
        self.hidden_layers = 3
        self.Wih = np.random.random((self.input_neurons,self.hidden_neurons))
        self.Whh = []
        for l in range(self.hidden_layers):
            self.Whh.append(np.random.random((self.hidden_neurons,self.hidden_neurons)))
        self.Who = np.random.random((self.hidden_neurons, self.input_neurons))
        self.bh = np.random.random(self.hidden_neurons)

    def reshape_vector(self,vector):
            return vector.reshape(3,3)

    def get_free_positions(self,vector):
        return np.abs(np.abs(vector)-1)

    def ReLu(input):
        return np.maximum(input,0)

    def sigmoid(self,x):
        output = 1/(1+np.exp(-x))
        return output

    def softmax(self,w, t = 1.0):
        e = np.exp(np.array(w) / t)
        dist = e / np.sum(e)
        return dist

    def forward_propagate(self,inputvector):
        #intermedieate states are all stored in h
        x = inputvector.flatten() #flatten the input vector
        s = np.dot(x,self.Wih) #apply weight matrix to first hiddens tate
        a = self.sigmoid(s)
        for l in range(self.hidden_layers): #iteratively do foreward porpagation for each hidden layer
            s = np.dot(a,self.Whh[l])+self.bh #
            a = self.sigmoid(s)
        s = np.dot(a,self.Who)
        p = self.softmax(s)
        f = self.get_free_positions(x)
        p_filtered = np.multiply(p,f)
        p_filtered = self.reshape_vector(p_filtered)
        x,y = np.unravel_index(p_filtered.argmax(),p_filtered.shape)
        return x,y

    def give_me_your_DNA(self):
        res = self.Wih.flatten()
        for l in range(self.hidden_layers):
            np.append(res,self.Whh[l].flatten())
        np.append(res,self.Who.flatten())
        np.append(res,self.bh.flatten())
        return res

    def set_new_DNA(self,new_DNA):
        none

    def get_name(self):
        return self.name

    def increase_turns(self):
        self.turns +=1

    def increase_wins(self):
        self.wins +=1

    def get_wins(self):
        return self.wins

    def get_move_coordinates(self):
        return self.x, self.y

    def get_moves(self):
        return self.turns

    def choose_next_move(self,field):
        self.x,self.y = self.forward_propagate(field)
        return self.x,self.y

    def choose_next_move_alt(self):
        while True:
            try:
                x,y = input('{}, please input coordinates for your next move (x,y):'.format(self.name)).split(',')
                break
            except ValueError:
                print('{}, the format of your input was not understood. Please try again and enter coordinates like this 1,1'.format(self.name))
        self.x,self.y = int(x)-1, int(y)-1
        return self.x,self.y

    def toogle_valid_move(self):
        self.valid_move = not(self.valid_move)

    def get_move_validity(self):
        return self.valid_move

class ttt_game:
    player_id_to_int = {0:1,1:-1}
    int_to_str = {0:' ',1:'X',-1:'O'}

    def __init__(self,player_0,player_1):
        self.game_over = False
        self.field = np.zeros((3,3),dtype=np.int8)
        self.turn = 0
        self.turns = 0
        self.max_turns = 9
        self.players = []
        self.players.append(player_0)
        self.players.append(player_1)

    def give_me_player_names(self):
        res = []
        for p in range(len(self.players)):
            res.append(self.players[p].get_name())
        return (res)


    def ask_for_move(self,playerId:int,field):
        self.players[playerId].choose_next_move(field)

    def check_move_validity(self):
        move_is_valid = False
        x_check, y_check = self.players[self.turn].get_move_coordinates()
        if x_check >= 0 and x_check <= 2 and y_check >= 0 and y_check <= 2:
            if self.field[x_check,y_check] == 0:
                move_is_valid = True
        if move_is_valid:
            self.players[self.turn].toogle_valid_move()
        else:
            print('{}, this move is not possible, please give me a nother one!'.format(self.players[self.turn].get_name()))

    def make_move(self):
        x_move, y_move = self.players[self.turn].get_move_coordinates()
        value_move = self.player_id_to_int[self.turn]
        self.field[x_move,y_move] = value_move
        self.players[self.turn].increase_turns()
        self.players[self.turn].toogle_valid_move()
        print('{} played ({},{})\n'.format(self.players[self.turn].get_name(),x_move+1,y_move+1))
        self.pretty_print_field()
        self.toogle_turns()
        self.turns+=1

    def toogle_turns(self):
        self.turn = abs(self.turn -1)

    def check_game_over(self):
        for x in range(3):
            if np.abs(np.sum(self.field[:,x])) ==3 or np.abs(np.sum(self.field[x,:])) ==3:#check rows and columns
                self.game_over = True
                self.turn = abs(self.turn -1)
            if np.abs(self.field[0,0]+self.field[1,1]+self.field[2,2]) == 3 or np.abs(self.field[0,2]+self.field[1,1]+self.field[2,0]) == 3: #check diagonals
                self.game_over = True
                self.turn = abs(self.turn -1)
            if self.turns >= self.max_turns:
                self.game_over = True

    def anounce_victor(self):
        if self.turns >= self.max_turns:
            print('The game ended in a draw!')
        else:
            self.players[self.turn].increase_wins()
            print('Game Over: {} has won after {} moves!'.format(self.get_current_player_name(),self.get_current_player_moves()))

    def get_current_player_name(self):
        return self.players[self.turn].get_name()

    def get_current_player_moves(self):
        return self.players[self.turn].get_moves()

    def pretty_print_field(self):
        pretty_field = ''
        for lines in self.field:
            for cells in lines:
                pretty_field += '|'
                pretty_field += self.int_to_str[cells]
            pretty_field += '|'
            pretty_field += '\n'
        print(pretty_field)