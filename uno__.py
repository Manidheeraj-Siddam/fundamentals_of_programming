import random

NUMBER_CARDS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
ACTION_CARDS = ["Skip", "Reverse", "Draw Two"]
WILD_CARDS = ["Wild", "Wild Draw Four"]
COLORS = ["Red", "Green", "Blue", "Yellow"]

def create_deck():
    deck = []
    for color in COLORS:
        for number in NUMBER_CARDS:
            deck.append((color, number))
            if number != "0":
                deck.append((color, number))
    for color in COLORS:
        for action in ACTION_CARDS:
            deck.append((color, action))
            deck.append((color, action))
    for wild in WILD_CARDS:
        for _ in range(4):
            deck.append(("wild", wild))
    return deck

def deal_cards(uno_deck, num_players):
    random.shuffle(uno_deck)
    hands = [[] for _ in range(num_players)]
    num_cards_per_player = 7
    for _ in range(num_cards_per_player):
        for i in range(num_players):
            hands[i].append(uno_deck.pop())
    return hands

def valid_cards(face_card, player_cards):
    playable_cards = []
    for card in player_cards:
        if card[1] == face_card[1] or card[0] == face_card[0] or card[0] == "wild":
            playable_cards.append(card)
    return playable_cards

def handle_special_cards(card, hands, deck, curr_player, direction):
    temp = direction
    if card[1] == "Reverse":
        direction *= -1
        temp = 0
    elif card[1] == "Skip":
         pass
    elif card[1] == "Wild Draw Four":
        draw_cards(hands, deck, curr_player + direction, 4)        
    elif card[1] == "Draw Two":
        draw_cards(hands, deck, curr_player + direction, 2)
    return direction, temp

def draw_cards(hands, deck, curr_player, num_cards):
    for _ in range(num_cards):
        player_index = (curr_player) % len(hands)
        hands[player_index].append(deck.pop())
    print(f"Player {curr_player + 1} hand: {hands[player_index]} \n")

def play(deck, hands):
    face_card = deck.pop()
    curr_player = 0
    direction = 1  
    while len(hands[curr_player]) != 0:
        temp = 0
        print(f"Face card: {face_card} \n")
        print(f"Player {curr_player + 1} hand: {hands[curr_player]}\n")
        playable_cards = valid_cards(face_card, hands[curr_player])
        
        if not playable_cards:
            print("No playable cards. Drawing from the deck.\n")
            hands[curr_player].append(deck.pop())
            curr_player = (curr_player + direction) % len(hands)
            continue
        else:
            print(f"Playable cards: {playable_cards} \n" )
            try:
                inp = int(input("Enter index of the card to play: ")) 
                played_card = playable_cards[inp]
                hands[curr_player].remove(played_card)
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid index.")
                continue
        
        if played_card[0] == "wild":
            color_choice = input("Choose color (Red, Green, Blue, Yellow): \n").capitalize()
            played_card = (color_choice, played_card[1])
        if played_card[1] == "Skip" or played_card[1] == "Reverse" or played_card[1] == "Draw Two" or played_card[1] == "Wild Draw Four":
          direction, temp = handle_special_cards(played_card, hands, deck, curr_player, direction)
        face_card = played_card
        print("Played:", face_card)
        if len(hands[curr_player]) == 0:
            print(f"Player {curr_player + 1} wins! \n")
            break
        curr_player = (curr_player + direction + temp) % len(hands)


uno_deck = create_deck()
hands = deal_cards(uno_deck,4)
play(uno_deck,hands)
