import random

suits = [chr(9824),chr(9827),chr(9829),chr(9830)]
ranks = [str(num) for num in range(2,11,1)]+['J','Q','K','A']
values = {str(num):num for num in range(2,11,1)}
values.update({'J':10,'Q':10,'K':10,'A':11})

playing = True

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.suit+self.rank#self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+card.__str__()
        return 'The Deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Chips:
    def __init__(self,total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet?\n'))
        except:
            print('Sorry please provede an integer')
        else:
            if chips.bet > chips.total:
                print('Sorry, you do not have enough chips! You have: {}'.format(chips.total))
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())

def hit_or_stand(deck,hand):
    global playing

    while True:
        x = input('Hit or Stand? Enter h or s\n')
        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print('Player Stands Dealer`s Turn')
            playing = False
        else:
            print('Sorry, I did not understand that, Please enter h or s only!')
            continue
        break

def show_some(player,dealer):
    print('DEALERS HAND:')
    print('one card hidden!')
    print(dealer.cards[1])
    print('\n')
    print('PLAYER HAND:')
    for card in player.cards:
        print(card)

def show_all(player,dealer):
    print('DEALERS HAND:')
    for card in dealer.cards:
        print(card)
    print('\n')
    print('PLAYER HAND:')
    for card in player.cards:
        print(card)

def player_busts(player,dealer,chips):
    print('BUST PLAYER!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('PLAYER WINS!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('PLAYER WINS! DEALER BUSTED!')
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print('DEALER WINS!')
    chips.lose_bet()

def push(player,dealer):
    print('Dealer and player tie! PUSH')



player_chips = Chips()
print('Welcome to BlackJack.\nYou have {} chips.'.format(player_chips.total))
while True:
    
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    take_bet(player_chips)

    show_some(player_hand,dealer_hand)

    while playing:
        hit_or_stand(deck,player_hand)
        show_some(player_hand,dealer_hand)
            
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break
            
    if player_hand.value <= 21:
        while dealer_hand.value < player_hand.value:
            print('Dealer hits!')
            hit(deck,dealer_hand)
        print('Dealer stands!')
        show_all(player_hand,dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    print('\nPlayer total chips are at: {}'.format(player_chips.total))

    new_game = input('Wold you like to play another hand? y/n\n')
    if new_game[0].lower() == 'y' and player_chips.total >0:
        playing = True
        continue
    else:
        print('Thank you for playing!')
        print('You left with {} chips!'.format(player_chips.total))
        break

