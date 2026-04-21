from random import shuffle
import csv
import os
import glob 

CARDS = {"Ace": 11, "Two": 2, "Three": 3, "Four": 4,
"Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10}
suit=['Ace',"Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King"]
win_loss=''
win_loss_tracker=[]
deck=[]
dealer_cards=[]
player_cards=[]
deck.extend(suit*4)
shuffle(deck)
loops=0
import os
import glob


extension = 'csv'

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = glob.glob(os.path.join(script_dir, "*.csv"))

strategy=[]
with open(csv_file[0],'r') as file:
    reader=csv.reader(file)
    for row in reader:
        strategy.append(row)
print (strategy)

def deal_with_aces(cards):
    temp=0
    for i in range(len(cards)):
        temp+=CARDS[cards[i]]
    if temp>21:
        return 1
    else:
        return 11

def calculate_score(cards):
    value=0
    for i in range(len(cards)):
        if cards[i]!="Ace":
                        value+=CARDS[cards[i]]
        else:
            value+=deal_with_aces(cards)
    return value

def deal(deck):
    values=[]
    dealer_cards.append(deck[0])
    deck.pop(0)
    dealer_cards.append(deck[0])
    deck.pop(0)

    player_cards.append(deck[0])
    deck.pop(0)
    player_cards.append(deck[0])
    deck.pop(0)
    values.append(calculate_score(player_cards))
    values.append(calculate_score(dealer_cards))
   
    return values
   
def hit(deck):
    values=[]
    player_cards.append(deck[0])
    deck.pop(0)
    values.append(calculate_score(player_cards))
    values.append(calculate_score(dealer_cards))
    return values
   
def stand(values,deck):
    while True:
        if values[0]>21:
            return 'l'
        elif values[1]>values[0]:
            return 'l'
        elif values[1]<17:
            values=[]
            dealer_cards.append(deck[0])
            deck.pop(0)
            values.append(calculate_score(player_cards))
            values.append(calculate_score(dealer_cards))
        elif values[1]>21:
            return 'w'
        elif values[1]>=17 and values[0]>values[1]:
            return 'w'
        elif values[0]==values[1]:
            return 'p'
   
def hit_stand_func(values):
    for i in range(len(strategy)):
        if strategy[i][0]==str(values[0]):
            row=i
            if dealer_cards[0] != 'Ace':
                return strategy[row][CARDS[dealer_cards[0]]]
            else:
                return strategy[row][1]
        elif values[0]<=11:
            return'h'
               
def game_loop(deck):
    if len(deck)<10:
        deck=[]
        deck.extend(suit*4)
        shuffle(deck)
    hitting=True
    values=deal(deck)
   
    while hitting:
        hit_or_stand=hit_stand_func(values)
        if hit_or_stand=='h':
            values=hit(deck)
        elif hit_or_stand=='s' or values[0]>21:
            hitting=False
    return stand(values,deck)
   
while loops<1:
    dealer_cards=[]
    player_cards=[]
    win_loss=game_loop(deck)
    win_loss_tracker.extend(win_loss)
    loops+=1
   
wins=win_loss_tracker.count('w')
losses=win_loss_tracker.count('l')
pushes=win_loss_tracker.count('p')

print('History:'+'\n'+str(win_loss_tracker))
print('Wins:',str(wins))
print('Losses:',str(losses))
print('Pushes:',str(pushes))
print('Win Rate:',str(((wins+(0.5*pushes))/(len(win_loss_tracker)))*100))

