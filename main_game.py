from random import shuffle
import csv
import os
import glob 

#Define DECK Componets
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
loops=0

#Finds CSV in same folder of the .py program 
program_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = glob.glob(os.path.join(program_dir, "*.csv"))

hard_strategy=[]
soft_strategy=[]

#Decides If User wants to play or simluate blackjack.
def sim_or_man():
    m_play=input('Do you want to simulate type s or manual type m?: ')
    if m_play=='m':
        return True
    elif m_play=='s': return False
    else: sim_or_man()
m_play=sim_or_man()


# Read and add soft and hard strategies to lists 
if not m_play:
    try:
        with open(csv_file[0],'r') as file:
            reader=csv.reader(file)
            for i,row in enumerate(reader):
                if i<= 18:   
                    hard_strategy.append(row)
                else:
                    soft_strategy.append(row)

    except:
        print("Cannot find Csv proper strategy make sure it is in same folder and is right layout!")
        os._exit(0)


#Calculates if the ace should be 1 or 11 
def deal_with_aces(cards):
         
    temp=0
    for i in range(len(cards)):
        temp+=CARDS[cards[i]]
    if temp>21:
        return 1
    else:
        return 11

#calculates the total value of the cards that were gave
def calculate_score(cards):
    value=0
    for i in range(len(cards)):
        if cards[i]!="Ace":
                        value+=CARDS[cards[i]]
        else:
            if cards.count('Ace')>=2:
                 temp=0
                 for i in range(len(cards)):
                    if i != 'Ace':
                        temp+=CARDS[cards[i]]
                 if temp+11+(cards.count('Ace')-1)>21:
                     value+=11
                 else:
                     value+=1
            value+=deal_with_aces(cards)
    return value

#Initial card dealing and setup
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

#Adds one card to the players hand
def hit(deck):
    values=[]
    player_cards.append(deck[0])
    deck.pop(0)
    values.append(calculate_score(player_cards))
    values.append(calculate_score(dealer_cards))
    return values

# Decides if that game was a win or a loss
def stand(values,deck):

    while values[1]<=21:
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
        if player_cards.count('Ace') == len(player_cards):
            if dealer_cards[0] != 'Ace':
                        return hard_strategy[9][CARDS[dealer_cards[0]]-1]
            else:
                    return hard_strategy[9][10]
        
        if player_cards.count('Ace')==1 and len(player_cards)==2 :
            
            for i in range(len(soft_strategy)):
                if soft_strategy[i][0]==str(values[0]-11):
                    row=i
                    if dealer_cards[0] != 'Ace':
                        return soft_strategy[row][CARDS[dealer_cards[0]]-1]
                    else:
                        return soft_strategy[row][10]   
        else:
            for i in range(len(hard_strategy)):
                if hard_strategy[i][0]==str(values[0]):
                    row=i
                    if dealer_cards[0] != 'Ace':
                        return hard_strategy[row][CARDS[dealer_cards[0]]-1]
                    elif player_cards.count('Ace')==2:
                        return 'h'
                    else:
                        return hard_strategy[row][1]   
    else:
        return input('Hit: h Stand:s Double:d Your Selection: ')

#Mainn Game it loops through for each hand simulated 
def game_loop(deck):
    #Shuffles in a new deck if cards are low 
    if len(deck)<10:
        deck=[]
        deck.extend(suit*4)
        shuffle(deck)

    hitting=True
    values=deal(deck)
    
    # Loops the game for as long as you are hitting
    while hitting and values[0]<=21:

        # Prints game info if playing manually
        if m_play:
            print("Dealer Cards:",'?',str(dealer_cards[0]))
            print('Dealer Value:',CARDS[dealer_cards[0]])
            print("Your Cards:")
            for i in player_cards:
                print(i)
            print('Your Value:',str(values[0]))

        hit_or_stand=hit_stand_func(values)

        if hit_or_stand!='d' and hit_or_stand!='s' and hit_or_stand!='h' :
            print('Make sure all input are in format of h,s,d')

        if hit_or_stand=='h':
            values=hit(deck)

        elif hit_or_stand=='s' or values[0]>21:
            hitting=False

        elif hit_or_stand == 'd':
            values=[]
            player_cards.append(deck[0])
            deck.pop(0)
            values.append(calculate_score(player_cards))
            values.append(calculate_score(dealer_cards))
            outcome=stand(values,deck)
    
            if outcome =='w':
                return 'dw'
            
            elif outcome=='l':
                return 'dl'
            
            else:
                return outcome
            
    return stand(values,deck)
   

#Runs the simulation for 100,000 hands for a accurate model of the outcome
while loops<100000:
    dealer_cards=[]
    player_cards=[]
    win_loss=game_loop(deck)
    if m_play:
        print(win_loss)
        print('\n\n\n')
    win_loss_tracker.append(win_loss)
    loops+=1

#Displays Final Result of the simulation
wins=win_loss_tracker.count('w')
d_wins=win_loss_tracker.count('dw')
losses=win_loss_tracker.count('l')
d_losses=win_loss_tracker.count('dl')
pushes=win_loss_tracker.count('p')

print('History:'+'\n'+str(win_loss_tracker))
print('Wins:',str(wins+d_wins))
print('Doubled Wins:',str(d_wins))
print('Losses:',str(losses+d_losses))
print('Doubled Losses:',str(d_losses))
print('Pushes:',str(pushes))

print('Win Rate:',str(((wins+(2*d_wins))/(d_wins+d_losses+wins+losses))*100))


