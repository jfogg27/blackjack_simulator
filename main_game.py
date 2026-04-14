from random import shuffle

CARDS = {"Ace": 11, "Two": 2, "Three": 3, "Four": 4,
"Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10}
dealer_cards=[]
player_cards=[]
suit=['Ace',"Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King"]
deck=[]
deck.extend(suit*4)
shuffle(deck)
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



    print (cards)
    print(value)
    return value


def deal():
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
    print(values)
    return values
def hit():
    values=[]
    player_cards.append(deck[0])
    deck.pop(0)


    values.append(calculate_score(player_cards))
    values.append(calculate_score(dealer_cards))

    print(player_cards)
    print(dealer_cards)
    print(values)
    check_game_state(values)
    
def stand():
    print("standing")
def hit_stand(player_cards,dealer_cards):
    i=''
    i=input("h or s")
    
    if i.lower()=="h":
        hit()
    elif i.lower()=="s":
        stand()
values=deal()
print(values[0])
def check_game_state(values):
    if values[0]<21:
        hit_stand(player_cards,dealer_cards)
    elif values[0]>21:
        stand()
        
check_game_state(values)

