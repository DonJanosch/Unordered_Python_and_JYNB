
# coding: utf-8

# In[1]:


from random import shuffle


# In[2]:


suits = [chr(int(i)) for i in '9824 9827 9829 9830'.split()]
ranks = '2 3 4 5 6 7 8 9 10 B D K A'.split()
rank_values = [i for i in range(2,11)]+[10 for _ in range(3)]+[11]
card_value_dict = dict(zip(ranks,rank_values))


# In[3]:


class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = card_value_dict[rank]
        
    def __str__(self):
        return self.get_card()
    
    def get_value(self):
        return self.value
    
    def get_card(self):
        return str(self.rank)+str(self.suit)


# In[4]:


class Deck:
    __all_cards = [(suit,rank) for suit in suits for rank in ranks]
    
    def __init__(self):
        self.__cards = [Card(suit,rank) for suit,rank in self.__all_cards]
        self.__remaining_cards = len(self.__cards)
        shuffle(self.__cards)
        self.__cards = (c for c in self.__cards)
        
    def __str__(self):
        return 'This move emptied the deck, need to make a new one!\n'+', '.join([c.get_card() for c in self.__cards])
    
    def get_cards(self,num_cards):
        self.__remaining_cards = max(self.__remaining_cards-num_cards,0)
        try:
            return [next(self.__cards) for _ in range(num_cards)]
        except:
            print('The Deck seems to be empty, please get reinitialize using .reinitializeDeck() !')
            
    def reinitializeDeck(self):
        self.__cards = [Card(suit,rank) for suit,rank in self.__all_cards]
        self.__remaining_cards = len(self.__cards)
        shuffle(self.__cards)
        self.__cards = (c for c in self.__cards)
        
    def how_many_remaining_cards(self):
        return self.__remaining_cards


# In[5]:


class Player:
    def __init__(self,name):
        self.name = name
        self.__cards = []
        self.__wins = 0
    
    def __str__(self):
        return 'Player '+self.name
    
    def recieve_cards(self,card_objects):
        self.__cards+=card_objects #Works because it already is a list we want to append
        
    def how_many_cards_do_you_have(self):
        return len(self.__cards)
        
    def play_card(self):
        try:
            return self.__cards.pop(0)
        except:
            print('{} as no more cards!'.format(self.name))
            return None
    
    def you_win(self,num_wins = 1):
        self.__wins+=num_wins
    
    def get_wins(self):
        return self.__wins


# In[6]:


class Game:
    def __init__(self,player_1_name = 'Player1', player_2_name = 'Player2'):
        self.deck = Deck()
        self.p1 = Player(player_1_name)
        self.p2 = Player(player_2_name)
        num_cards_per_player = self.deck.how_many_remaining_cards() // 2
        self.p1.recieve_cards(self.deck.get_cards(num_cards_per_player))
        self.p2.recieve_cards(self.deck.get_cards(num_cards_per_player))
        self.__draws = 0
        self.__rounds = 0
        
    def status(self):
        p1_num_cards = self.p1.how_many_remaining_cards()
        print(p1_num_cards)
        
    def play(self):
        match_report = ''
        p1_card = self.p1.play_card()
        p2_card = self.p2.play_card()
        if p1_card != None and p2_card != None:
            match_report+= '\nGame-Round: '+str(self.__rounds)+'\n'
            p1_picture, p1_value = p1_card.get_card(), p1_card.get_value()
            match_report+= '{} drew {} which is worth {}.\n'.format(self.p1.name,p1_card,p1_value)
            p2_picture, p2_value = p2_card.get_card(), p2_card.get_value()      
            match_report+= '{} drew {} which is worth {}.\n'.format(self.p2.name,p2_card,p2_value)


            if p1_value > p2_value:
                self.p1.you_win(self.__draws+1)
                match_report+='{} won {} cards!'.format(self.p1.name,self.__draws+1)
                self.__draws = 0
            elif p1_value == p2_value:
                self.__draws+=1
                match_report+='DRAW! Cards go on the stack. Currentyl {} cards are on the stack.'.format(self.__draws)
            else:
                self.p2.you_win(self.__draws+1) 
                match_report+='{} won {} cards!\n'.format(self.p2.name,self.__draws+1)
                self.__draws = 0
            self.__rounds+=1
        else:
            match_report+= 'The game ended\n'
            p1_wins = self.p1.get_wins()
            match_report+='{} won {} cards\n'.format(self.p1.name,p1_wins)
            p2_wins = self.p2.get_wins()
            match_report+='{} won {} cards\n'.format(self.p2.name,p2_wins)
            if p1_wins > p2_wins:
                winner = self.p1.name
                match_report+='{} won the game!\n'.format(winner)
            elif p1_wins == p2_wins:
                match_report+='The game ended in a DRAW!\n'
            else:
                winner = self.p2.name
                match_report+='{} won the game!\n'.format(winner)
        print(match_report)
                


# In[7]:


g = Game('Sepp','Hans')


# In[8]:


for x in range(30):
    print('\nLoop-Run:',x)
    g.play()

