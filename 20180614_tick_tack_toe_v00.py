#0. PROGRAMM DESCRIPTION. Some information about the program to give other viewers a clue of what they are about to encounter
'''A simple Tick-Tack-Toe game... quick and dirty
Autor: Jan Macenka
Last updated: 15-06-2018
Scripted for Python-Version: Python 3.5.4'''

#1. FUNCTION DEFFINITIONS. Do you have a Idea why these should be before the rest of the script? ;-)
def print_board(): #Funciton for printing the current status of the game-board to the console
    '''Function that prints the current state of the game-board to the console. No return value.'''
    print('') #Print an empty line before the board for better readability
    for i in range(3): #The board is 3x3 in size. Using a For-Loop with range(3) to print it
        print('|{}|{}|{}|'.format(board[6-i*3],board[7-i*3],board[8-i*3])) #Each line is accessing the list 'board' to get the symbols for printing. Initially the board is filled with ' ' empty strings.
    print('') #Print an empty line after the board for better readability

def get_next_move(): #Function to ask the player for his next move and updating all variables acordingly
    '''Function that asks the player in turn to choose one of the remaining possibel board-positions as next move and updates the board acordingly. No function-input-parameters.'''
    global turns, board #Required to access the global variables
    player_id = turns%2 + 1 #Determine whos turn it is by (Round-Nr. modulo 2) + 1 - This expression will alternatingly yield 1 or 2 
    choice = '' #Initialize an empty string container to hold the players input
    while not choice in possible_moves: #Check if the players input is a valid move. If not, ask for another input
        choice = input('Please chose one of the following board-positions and hit enter:\n{}\nPlayer{}\'s choice: '.format(' '.join(x for x in possible_moves),player_id)) #Ask the player for a input and present to him the list of possible choices which are left to chose from.
    board[int(choice)-1] = player_id_to_player_symbol[player_id] #Update the board-status at the position the player picked (-1 because of zero-indexing) with the symbol of the player in turn
    possible_moves.remove(choice) #Remove the position the player picked form the list of possible choices
    turns+=1 #Increment the counter by one to keep track how many turns there were in the game

def check_game_over(): #Function to check whether one of the players has won the game
    '''Function that check wheter the game can continue and returns a bool value. True = continue, False = game over. No function-input-parameters.'''
    checking = [[board[idx] for idx in combination] for combination in winning_position_combinations] #Make a list of lists with all the possible combinations wich can be achieved to win the game and fill them with the current status of the game-board
    for pos in checking: #Loop over all the generated lists
        if pos in winning_conditions: #Check wether one of them matches a winning-condition
            print('GAME OVER: Player{} won after {} turns!'.format((turns-1)%2+1,turns)) #If so, anounce geme over and player id
            return False #Also return False to stop the games while-loop
    if turns == 9: #If no winning-condition is met, the game can still be over if all the positions are taken, so check for that
        print('GAME OVER: Draw - nobody won.') #If so, anounce game over with a draw
        return False #In this case return False to stop the game
    else: #If none of the conditions were met to end the game
        return True #Return True to continue the game

def main(): #The 'body' of a script or program is usually encapsulated in a function called main. This step is also a good thing to force the programmer to structure his code properly.
    '''The main-function which holds the body of the programm and starts the entire thing. No function-input-parameters.'''
    print_board() #Initially print the empty board to show the user
    while check_game_over(): #Start a while-loop for the game and each time check wether a game-over conditon is met using the 'check_game_over()'-Method. If the game is over this function will also make a print to anounce the winner.
        get_next_move() #If the game is not over, ask the player in turn for his next move and update the board-state accordingly
        print_board() #Print the current state of the board    

#2. VARIABLE DECLARATION. Initializing the required global game-variables
print('Welcome, lets play some Tic-Tac-Toe!\n') #Greetings to the user and tell them what we are about to do
symbols = [str(input('Player{} please pick any symbol and hit enter.\n'.format(idx+1)))[0] for idx in range(2)] #Get input from 2 players and take the first character of the string, return a list with the payers symbols
player_id_to_player_symbol = dict(zip([1,2],symbols)) #Make a dictionary that maps the player_id to the player_symbol for look-up
turns = 0 #Keep track of how many turns there were in the game
board = [' ' for _ in range(9)] #Create new list as board with all the 9 possible positions initialized with ' '
possible_moves = [str(x) for x in range(1,10)] #Create a list with possible moves for the players to pick from
winning_position_combinations = [[x+y*3 for x in range(3)] for y in range(3)]+[[x*3+y for x in range(3)] for y in range(3)]+[[0,4,8],[2,4,6]] #Create a list of all possible winning-combinations
winning_conditions = [[sym for _ in range(3)] for sym in symbols] #Create a list of lists with all the possible winnig combinations like e.g. ['x','x','x']

#3. CALLING THE MAIN FUCNTION. Starting a while-loop to run the game
main() #Callling the programs main function as last step (typical "best practise" behaviour in programming)
