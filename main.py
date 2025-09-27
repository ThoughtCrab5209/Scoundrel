# imports
import random
from player import Player


# variables


# functions
def take_player_action(cards, player):

    print("Input the number of the card to interact with, or input '0' to skip this floor")

    # 1. pick a card
    user_input = input("Select a card: ")

    # 2. process
    if user_input == '0' and player.last_floor_skipped == 0:
        player.last_floor_skipped = 1
        cards = []
    
    else:            
        card = cards[int(user_input) - 1]
        split_card = card.split("-")
        rank = split_card[0]
        suit = split_card[1]

        match suit:
            case "H":
                player.heal(int(rank))
            case "D":
                player.change_weapon(int(rank))
            case "S":
                player.fight(rank)
            case "C":
                player.fight(rank)

        # 3. remove card from cards
        cards.remove(card)


    # 4. return cards
    return cards


def translate_card(card:str):
    
    card = card.split("-")
    rank = card[0]
    suit = card[1]

    match rank:
        case "2":
            rank = "Two"
        case "3":
            rank = "Three"
        case "4":
            rank = "Four"
        case "5":
            rank = "Five"
        case "6":
            rank = "Six"
        case "7":
            rank = "Seven"
        case "8":
            rank = "Eight"
        case "9":
            rank = "Nine"
        case "0":
            rank = "Ten"
        case "J":
            rank = "Jack"
        case "Q":
            rank = "Queen"
        case "K":
            rank = "King"
        case "A":
            rank = "Ace"

    match suit:
        case "H":
            suit = "Hearts"
        case "D":
            suit = "Diamonds"
        case "S":
            suit = "Spades"
        case "C":
            suit = "Clubs"


    return f"{rank} of {suit}"


def print_floor_ui(cards, floor_number: int, player):

    print(f"=========== Floor {floor_number} ===========\n")
    
    for i in range (0, cards.__len__()):
        print(f"[{i+1}] {translate_card(cards[i])}")

    print("\n===============================\n")
    
    print(f"HEALTH: {player.health}")
    print(f"WEAPON: {player.weapon}")
    if player.last_fought_enemy == 15:
        print("WEAPON: NONE")
    else:
        print(f"LAST FOUGHT ENEMY: {player.last_fought_enemy}")

    print("\n===============================\n")


def shuffle_deck():

    deck = [
        "2-H", "3-H", "4-H", "5-H", "6-H", "7-H", "8-H", "9-H", "0-H",
        "2-D", "3-D", "4-D", "5-D", "6-D", "7-D", "8-D", "9-D", "0-D",
        "2-S", "3-S", "4-S", "5-S", "6-S", "7-S", "8-S", "9-S", "0-S", "J-S", "Q-S", "K-S", "A-S",
        "2-C", "3-C", "4-C", "5-C", "6-C", "7-C", "8-C", "9-C", "0-C", "J-C", "Q-C", "K-C", "A-C"
    ]

    shuffled_deck = []

    while deck.__len__() > 0:
        # pick the next card
        card_index = random.randint(0, deck.__len__())

        # add the card to the shuffled deck
        shuffled_deck.append(deck[card_index - 1])

        # remove it from the deck
        deck.remove(deck[card_index - 1])

    return shuffled_deck


# main
def main():
    random.seed(0000)
    player = Player()

    # generate the deck
    game_deck = shuffle_deck()

    current_floor = []
    floor_count = 0
    actions_remaining = 4
    

    # continue the gameplay loop while there are still cards to be drawn
    while game_deck.__len__() > 0 and player.health > 0:
        
        # set values
        actions_remaining = 4
        player.previously_healed = False
        player.check_floor_skip()

        # increment floor count by 1
        floor_count += 1

        # generate the next floor
        for i in range(0, (5 - current_floor.__len__())):
            current_floor.append(game_deck.pop(0))


        while actions_remaining > 0 and player.health > 0:
            # print the next floor
            print_floor_ui(current_floor, floor_count, player)

            # actions
            current_floor = take_player_action(current_floor, player)
            
            if current_floor == []:
                actions_remaining = 0
            else:
                actions_remaining -= 1
    

# run the program
main()