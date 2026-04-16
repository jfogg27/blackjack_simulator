from random import shuffle

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
strategy=[['','11','2','3','4','5','6','7','8','9','10'],['21','s','s','s','s','s','s','s','s','s','s'],['20','s','s','s','s','s','s','s','s','s','s'],
['19','s','s','s','s','s','s','s','s','s','s'],['18','s','s','s','s','s','s','s','s','s','s'],['17','s','s','s','s','s','s','s','s','s','s'],
['16','h','s','s','s','s','s','h','h','h','h'],['15','h','s','s','s','s','h','h','h','h','h'],['14','h','s','s','s','h','h','h','h','h','h'],['13','h','s','s','h','h','h','h','h','h','h'],['12','h','s','h','h','h','h','h','h','h','h']
,['11','h','h','h','h','h','h','h','h','h','h']]








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
    
def stand(values):
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
        elif values[1]>=17 and values[0]>values[1]:
            return 'w'
            
    
def hit_stand_func(values):
        print(values[0])
        for i in range(len(strategy)):
            if strategy[i][0]==str(values[0]):
                print('works')
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
    print("Dealer Cards: "+ dealer_cards[0]+', ? Value:'+str(CARDS[dealer_cards[0]]))
    print("Your Cards: "+player_cards[0]+","+player_cards[1]+" Value: "+ str(values[0]))
    print('Left in deck:'+str(len(deck)))
    
    
    while hitting:
        hit_or_stand=hit_stand_func(values)
        print(hit_or_stand)
        if hit_or_stand=='h':
            values=hit(deck)
            print("Dealer Cards: "+ dealer_cards[0]+', ? Value:'+str(CARDS[dealer_cards[0]]))
            print("Your Cards:")
            
            for i in range(len(player_cards)):
              print(player_cards[i-1])
            print('Value: '+str(values[0]))
            
        elif hit_or_stand=='s' or values[0]>21:
            hitting=False
            
    return stand(values)
    
while loops<10:
    dealer_cards=[]
    player_cards=[]
    win_loss=game_loop(deck)
    win_loss_tracker.extend(win_loss)
    print(win_loss_tracker)
    loops+=1
