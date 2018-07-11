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
import TTT_Class as game

def get_worst_player_id(fitness_array):
    return np.unravel_index(fitness_array.argmin(),fitness_array.shape)[0]

def choose_parent_id(fitness_array):
    return np.random.choice(np.arange(len(fitness_array)),size = 2,p=normalize(fitness_array),replace=False) #Propability based choice without replacement

def normalize(x):
    x = abs(x)
    dist = x / np.sum(x)
    return dist

def create_offspring(parents,players,mutation_treshhold=0.02):
    mother_id,father_id = parents
    mother_genes = players[mother_id].give_me_your_DNA()
    father_genes = players[father_id].give_me_your_DNA()
    number_of_genes = len(mother_genes)
    cross_over_point = np.random.randint(number_of_genes)
    child = np.append(mother_genes[:cross_over_point],father_genes[cross_over_point:])
    mut_mult = np.random.random((child.size))
    mut_add = mut_mult
    mut_mult[mut_mult>=mutation_treshhold] = 1
    mut_add[mut_add>=mutation_treshhold] = 0
    child = np.multiply(child,mut_mult)+mut_add
    return child

def play_normal_game():
    #Initialize the players
    #player_1 = player('Human')
    #player_2 = player('AI')
    player_1 = players[0]
    player_2 = players[1]

    #Initialize the game
    my_game = game.ttt_game(player_1,player_2)
    #Start playing
    print('Starting a new Game: {} vs {}\n'.format(my_game.players[0].get_name(),my_game.players[1].get_name()))
    print(my_game.pretty_print_field())
    while True:
        while not(my_game.players[my_game.turn].get_move_validity()):
            my_game.ask_for_move(my_game.turn)
            my_game.check_move_validity()
        my_game.make_move()
        my_game.check_game_over()
        if my_game.game_over == True:
            my_game.anounce_victor()
            break

def main():
    #Initialize the players
    number_of_players = 5
    max_generations = 100
    players = []
    matchups = []
    for p in range(number_of_players):
        new_name = 'AI_'+str(p)
        players.append(game.player(new_name))
        for p2 in range(p+1,number_of_players):
            matchups.append((p,p2))

    number_of_games = len(matchups)
    match_results = []

    #Initialize the game
    for gen in range(max_generations):
        players_fitness = np.zeros(len(players),dtype=np.int8)
        for g in range(number_of_games):
            print('Starting match Nr. {} of {}'.format(g+1,number_of_games))
            player_1_id = matchups[g][0]
            player_2_id = matchups[g][1]
            my_game = game.ttt_game(players[player_1_id],players[player_2_id])
            #Start playing
            print('Starting a new Game: {} vs {}\n'.format(*my_game.give_me_player_names()))
            print(my_game.pretty_print_field())
            while True:
                while not(my_game.players[my_game.turn].get_move_validity()):
                    my_game.ask_for_move(my_game.turn,my_game.field*my_game.player_id_to_int[my_game.turn])
                    my_game.check_move_validity()
                my_game.make_move()
                my_game.check_game_over()
                if my_game.game_over == True:
                    my_game.anounce_victor()
                    players[player_1_id] = my_game.return_player_from_match()[0]
                    players[player_2_id] = my_game.return_player_from_match()[1]
                    break

        for p in range(len(players)):
            p_wins = players[p].get_wins()
            print('Player {} has {} wins.'.format(players[p].get_name(),p_wins))
            players_fitness[p] = p_wins

        parents = choose_parent_id(players_fitness)
        mother, father = parents
        child = create_offspring(parents,players)
        worst_creature_id = get_worst_player_id(players_fitness)
        print('After generation {} the offspring of Player{} and Player{} replaced Player{}'.format(gen+1,mother,father,worst_creature_id))
        players[worst_creature_id].set_new_DNA(child)
        match_results.append(players_fitness)

    with open('restults.txt','w') as doc:
        for res in match_results:
            doc.write("{}\n".format(res))


if __name__ == '__main__':
    main()
