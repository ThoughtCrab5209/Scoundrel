# --- imports ---
import random
import sys
from player import Player


# --- functions ---
def pick_weapon(player, value):
    may_fight_with_weapon = False
    fight_type = ""
    
    if value == "J":
        value = 11
    elif value == "Q":
        value = 12
    elif value == "K":
        value = 13
    elif value == "A":
        value = 14
    else:
        value = int(value)

    if player.weapon != 0 and value < player.last_fought_enemy:
        may_fight_with_weapon = True
    else:
        may_fight_with_weapon = False

    while fight_type != "B" and fight_type != "W":
        if not may_fight_with_weapon:
            fight_type = "B"
            player.fight_with_hands(value)
        else:
            fight_type = input("Fight using your weapon (W) or barehanded (B)? ").capitalize()
            if fight_type == "W":
                player.fight_with_weapon(value)
            elif fight_type == "B":
                player.fight_with_hands(value)
            else:
                pass


def take_player_action(cards, player):
    if player.previous_floor_skipped == 0:
        print("Input the number of the card to interact with\n")
    else:
        print("Input the number of the card to interact with; This floor can not be skipped\n")

    user_input = input("Select a card: ")

    if user_input == '0':
        player.skip_floor()
        cards = []
    
    else:
        try:
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
                    pick_weapon(player, rank)
                case "C":
                    pick_weapon(player, rank)

            cards[int(user_input) - 1] = None

        except:
            player.actions += 1
        
    return cards


def print_player_stats(player):
    print("\n===============================\n")
    print(f"ACTIONS: {player.actions}")
    print(f"HEALTH: {player.health}")
    print(f"WEAPON: {player.weapon}")

    if player.last_fought_enemy == 15:
        print("LAST FOUGHT ENEMY: NONE")
    else:
        print(f"LAST FOUGHT ENEMY: {player.last_fought_enemy}")

    print("\n===============================\n")


def translate_card_shorthand(card:str):
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
        case "10":
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
    
    if not player.previous_floor_skipped:
        print("[0] Skip")
    else:
        print("[0]")

    for i in range (0, 5):
        try:
            print(f"[{i+1}] {translate_card_shorthand(cards[i])}")
        except:
            print(f"[{i+1}]")

    print_player_stats(player)


def check_player_floor_skips(player):
    if player.previous_floor_skipped and player.current_floor_skipped:
        return False
    
    return True


def shuffle_deck():
    deck = [
        "2-H", "3-H", "4-H", "5-H", "6-H", "7-H", "8-H", "9-H", "10-H",
        "2-D", "3-D", "4-D", "5-D", "6-D", "7-D", "8-D", "9-D", "10-D",
        "2-S", "3-S", "4-S", "5-S", "6-S", "7-S", "8-S", "9-S", "10-S", "J-S", "Q-S", "K-S", "A-S",
        "2-C", "3-C", "4-C", "5-C", "6-C", "7-C", "8-C", "9-C", "10-C", "J-C", "Q-C", "K-C", "A-C"
    ]

    shuffled_deck = []

    while deck.__len__() > 0:
        card_index = random.randint(0, deck.__len__())
        shuffled_deck.append(deck[card_index - 1])
        deck.remove(deck[card_index - 1])

    return shuffled_deck


# --- main ---
def main():
    # Code obtained from: https://stackoverflow.com/questions/5012560/how-to-query-seed-used-by-random-random
    seed = random.randrange(sys.maxsize)
    random.Random(seed)

    player = Player()
    game_deck = shuffle_deck()
    current_floor = []
    floor_count = 0

    # gameplay loop
    while (game_deck.__len__() > 0 or current_floor.__len__() > 0) and player.health > 0 and check_player_floor_skips(player):
        # generate the next floor
        for i in range(0, (5 - current_floor.__len__())):
            try:
                current_floor.append(game_deck.pop(0))
            except:
                pass

        floor_count += 1
        player.reset_status(current_floor.__len__())

        # player action loop
        while player.actions > 0 and player.health > 0:
            print_floor_ui(current_floor, floor_count, player)

            current_floor = take_player_action(current_floor, player)
            
            if current_floor == []:
                player.actions = 0
            else:
                player.actions -= 1
        
        # clear the floor if possible
        try:
            current_floor.remove(None)
            current_floor.remove(None)
            current_floor.remove(None)
            current_floor.remove(None)
        except:
            pass
    
    # results
    print_player_stats(player)

    if player.health != 0 and check_player_floor_skips(player):
        print("YOU WIN")
    elif player.health == 0:
        print("YOU LOSE BY DYING")
    elif not check_player_floor_skips(player):
        print("YOU LOSE BY SKIPPING TWO SIMULTANEOUS FLOORS")
    else:
        print("UNHANDLED END STATE")

    print(f"Seed for this run: {seed}")

# run the program
main()