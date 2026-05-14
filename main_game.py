from random import shuffle
import csv 
import os
import glob 
import time 
from collections import deque

#Define DECK Componets and other global variables 
CARDS = {"Ace": 11, "Two": 2, "Three": 3, "Four": 4,
"Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10}
suit=['Ace',"Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King"]
deck=[]
deck.extend(suit*4)

win_loss=''
win_loss_tracker=[]

dealer_cards=[]
player_cards=[]

shuffle(deck)
deck = deque(deck)
loops=0

#Finds CSV in same folder of the .py program
program_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = glob.glob(os.path.join(program_dir, "*.csv"))

hard_strategy=[]
soft_strategy=[]

#Tool to see runtime of code
def runtime(func):
    def wrapper(*args,**kwargs):
        start_time=time.perf_counter()
        result = func(*args, **kwargs)
        end_time=time.perf_counter()
        print(f'{func.__name__}: {end_time-start_time:6f}')
        return result
    return wrapper

#Decides If User wants to play or simluate blackjack and also how many hands they want to play or simulate.
def sim_or_man():
    m_play=input('Do you want to simulate hands of blackjack with the csv in this folder type s or do you want to manually play blackjack type m?: ')
    if m_play=='m':
        return True
    elif m_play=='s': return False
    else: sim_or_man()
m_play=sim_or_man()

#Decides how many hands to sim or play
def how_many():
    try:
        if m_play==False: 
            sim_hands=input('How many hands should be simulated 100,000 , 200,000 .ect: ')
            return int(sim_hands)
        else: 
            sim_hands=input('How many hands do you want to play? ')
            return int(sim_hands)
    except:
        print("Please Enter A Number: ")
        return how_many()
sim_hands=how_many()

# Read and add soft and hard strategies to lists and then convert those lists to dictionaries for faster access
if not m_play:
    try:
        with open(csv_file[0],'r') as file:
            reader=csv.reader(file)
            for i,row in enumerate(reader):
                if i<= 18:   
                    hard_strategy.append(row)
                else:
                    soft_strategy.append(row)
        hard_strategy = {row[0]: row for row in hard_strategy}
        soft_strategy = {row[0]: row for row in soft_strategy}

    except:
        print("Cannot find Csv proper strategy make sure it is in same folder and is right layout!")
        os._exit(0)

# If manually playing prints the current state of the game
def display_game_state(values):
    if m_play:
            print('\n\n\n\n')
            print("Dealer Cards:")
            print(dealer_cards[1])
            print('Dealer Value:',str(CARDS[dealer_cards[1]))
            print("Your Cards:")
            for i in player_cards:
                print(i)
            print('Your Value:',str(values[0]))

# Calculates the total value of cards inputed
def calculate_score(cards):
    value = sum(CARDS[c] for c in cards)
    aces = cards.count('Ace')
    while value > 21 and aces:
        value -= 10   
        aces -= 1
    return value

#Initial card dealing and setup of the game it gives the player and dealer two cards and then calculates the score of those cards and returns them in a list
def deal(deck):
    for _ in range(2):
        dealer_cards.append(deck.popleft())
        player_cards.append(deck.popleft())
    return [calculate_score(player_cards),calculate_score(dealer_cards)]

# Decides if that game was a win or a loss or a push and also handles the dealers hand if you stand
def stand(values,deck):
    while values[1]<=21:
        display_game_state(values)
        if values[0]>21:
            return 'b'
        elif values[1]>values[0]:
            return 'l'
        elif values[1]<17:
            dealer_cards.append(deck.popleft())
            values[1]=calculate_score(dealer_cards)
           
        elif values[1]>=17 and values[0]>values[1]:
            return 'w'
        elif values[0]==values[1]:
            return 'p'
    if m_play:
            print('\n\n\n\n')
            print("Dealer Cards:")
            for i in dealer_cards:
                print(i)
            print('Dealer Value:',str(values[1]))
            print("Your Cards:")
            for i in player_cards:
                print(i)
            print('Your Value:',str(values[0]))
    return 'w'

#Csv file decides if you should stay or hit or double
def hit_stand_func(values):
    if not m_play:
        player_cards_len = len(player_cards)
        ace_amount = player_cards.count('Ace')
        
        dealer_col = 10 if dealer_cards[0] == 'Ace' else CARDS[dealer_cards[0]] - 1

        if ace_amount == player_cards_len:
            return hard_strategy['9'][dealer_col]

        if ace_amount == 1 and player_cards_len == 2:
            return soft_strategy[str(values[0] - 11)][dealer_col]
        else:
            row = hard_strategy.get(str(values[0]))
            if row is None: return 'h'
            return 'h' if ace_amount == 2 else row[dealer_col]
    else:
        return input('Hit: h Stand:s Double:d Your Selection: ')

#Main Game it loops through for each hand simulated or played and also shuffles in a new deck if the cards are low and also prints game info if playing manually 
def game_loop(deck):

    #Shuffles in a new deck if cards are low  
    if len(deck) < 20:
        new_cards = suit * 4
        shuffle(new_cards)
        deck.extend(new_cards)

    hit_or_stand=''
    hitting=True
    values=deal(deck)
    
    # Loops the game for as long as you are hitting 
    while hitting and values[0]<=21 and hit_or_stand != 's':

        # Prints game info if playing manually
        display_game_state(values)

        hit_or_stand=hit_stand_func(values)   

        try:
            if hit_or_stand=='h': 
                player_cards.append(deck.popleft())
                values[0]=calculate_score(player_cards)
            elif hit_or_stand == 'd':
                player_cards.append(deck.popleft())
                values[0]=calculate_score(player_cards)
                outcome=stand(values,deck)
                if outcome=='p': return outcome
                return str('d'+outcome )   
        except: 
            print('Make sure all input are in format of h,s,d')
            os._exit(0)
    return stand(values,deck)
   

#Runs the simulation for # hands for a accurate model of the outcome 
while loops<int(sim_hands):
    dealer_cards = []
    player_cards = []
    
    win_loss= game_loop(deck)
    win_loss_tracker.append(win_loss)

    if loops % 1000000 == 0:
        print('Hands simulated:',str(loops))
        
    if m_play:
        print('\n\n\n')
        print(f"Last Game Outcome: {win_loss}")
    loops += 1

#Displays Final Result of the simulation
wins=win_loss_tracker.count('w')
d_wins=win_loss_tracker.count('dw')

losses=win_loss_tracker.count('l')+win_loss_tracker.count('b')
busts=win_loss_tracker.count('b')
d_losses=win_loss_tracker.count('dl')

pushes=win_loss_tracker.count('p')

print('\n\n\nWins:',str(wins))
print('Doubled Wins:',str(d_wins))
print('Losses:',str(losses))
print('You busted:',str(busts))
print(f'You busted: {(busts/len(win_loss_tracker))*100:.2f}% of games')
print('Doubled Losses:',str(d_losses))
print('Pushes:',str(pushes))
print(f'Win Rate: {((wins+(2*d_wins))/(d_wins+d_losses+wins+losses+d_losses))*100:.2f}%')
input('Press Enter to exit Program: ')
