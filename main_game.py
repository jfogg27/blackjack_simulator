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
if m_play==False:
    sim_hands=input('How many hands should be simulated (300,000 per second) .ect: ')
else:
    sim_hands=input('How many hands do you want to play? ')
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
    ace_amount=cards.count('Ace')
    len_cards=len(cards)
    for i in range(len_cards):
        if cards[i]!="Ace":
            value+=CARDS[cards[i]]
        else:
            if ace_amount>=2:
                 temp=0
                 for i in range(len_cards):
                    if i != 'Ace':
                        temp+=CARDS[cards[i]]
                 if temp+(ace_amount-1)>10:
                     value+=11
                 else:
                     value+=1
            value+=deal_with_aces(cards) 
    return value

#Initial card dealing and setup
def deal(deck):
    for _ in range(2):
        dealer_cards.append(deck.pop(0))
        player_cards.append(deck.pop(0))
    return [calculate_score(player_cards),calculate_score(dealer_cards)]

#Adds one card to the players hand
def hit(deck):
    player_cards.append(deck.pop(0))
    return calculate_score(player_cards)

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
            dealer_cards.append(deck.pop(0))
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
        player_cards_len=len(player_cards)
        ace_amount=player_cards.count('Ace')

        if ace_amount == player_cards_len:
            if dealer_cards[0] != 'Ace': 
                return hard_strategy[9][CARDS[dealer_cards[0]]-1]
            else: 
                return hard_strategy[9][10]
        
        if ace_amount==1 and player_cards_len==2 :
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
                    elif ace_amount==2:
                        return 'h'
                    else:
                        return hard_strategy[row][1]   
    else:
        return input('Hit: h Stand:s Double:d Your Selection: ')

#Mainn Game it loops through for each hand simulated 
def game_loop(deck):

    
    #Shuffles in a new deck if cards are low 
    if len(deck)<20:
        deck.extend(suit*4)
        shuffle(deck)

    hit_or_stand=''
    hitting=True
    values=deal(deck)
    
    # Loops the game for as long as you are hitting
    while hitting and values[0]<=21 and hit_or_stand != 's':

        # Prints game info if playing manually
        if m_play: 
            print("Dealer Cards:",'?',str(dealer_cards[0]))
            print('Dealer Value:',CARDS[dealer_cards[0]])
            print("Your Cards:")
            for i in player_cards: print(i)
            print('Your Value:',str(values[0]))
        
        hit_or_stand=hit_stand_func(values)   

        #try:
        if hit_or_stand=='h': 
                values[0]=hit(deck)
        elif hit_or_stand == 'd':
                player_cards.append(deck.pop(0))

                values[0]=calculate_score(player_cards)
                outcome=stand(values,deck)
                if outcome=='p': return outcome
                return str('d'+outcome )   
        #except: 
            #print('Make sure all input are in format of h,s,d')
            #os._exit(0)
    return stand(values,deck)
   

#Runs the simulation for # hands for a accurate model of the outcome
while loops<int(sim_hands):
    dealer_cards = []
    player_cards = []
    
    win_loss= game_loop(deck)
    win_loss_tracker.append(win_loss)

    if loops % 300000 == 0:
        print('hands simulated:',str(loops))
    if m_play:
        print(win_loss)
        print('\n\n\n')    
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
print('You busted:',str((busts/len(win_loss_tracker))*100)+'%','of games')
print('Doubled Losses:',str(d_losses))
print('Pushes:',str(pushes))
print('Win Rate:',str(((wins+(2*d_wins))/(d_wins+d_losses+wins+losses+d_losses))*100))
input('Press Enter to exit Program: ')
