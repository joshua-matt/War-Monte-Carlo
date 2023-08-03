import random # Shuffling
import time # Timing sampling runs
import datetime # Creating file names for exporting data
import matplotlib.pyplot as plt # Showing game length distribution
import numpy as np

## DATA VARIABLES ##
read_file = True
fname = "08-02-2023 170929 (100000 samples).txt"

## SIMULATION VARIABLES ##
WAR_N = 3 # Number of cards at stake from each side in a war
n_games = 100000
game_lengths = []

# Procedure:
#   game
# Purpose:
#   To play a game of War starting with a shuffled deck
# Inputs:
#   None
# Outputs:
#   The number of turns in the entire simulated game
def game(war_n):
    deck = [i for i in range(2, 15) for j in range(4)] # Suits don't matter in War
    random.shuffle(deck)
    deck1 = deck[:26]
    deck2 = deck[26:]

    length = 0

    while len(deck1) != 52 and len(deck2) != 52:
        deck1, deck2 = play_turn(deck1, deck2, [], war_n=war_n)
        length += 1
        if length > 5000:
            print(deck1[0] > deck2[0])

    return length

# Procedure:
#   play_turn
# Purpose:
#   To simulate one turn of a game of War (including nested wars using recursion)
# Inputs:
#   deck1 - the deck of player 1, where the top of the deck is the beginning of the list
#   deck2 - the deck of player 2, " "
#   to_append - the list of cards to give the winner, typically initialized as empty
# Outputs:
#   decks - a tuple of the updated decks (new_deck1, new_deck2)
def play_turn(deck1, deck2, to_append, war_n=2): # In this interpretation, any turn that starts with a war, no matter how many subsequent wars follow, is still counted as only one turn.
    p1_card = deck1[0]
    p2_card = deck2[0]

    if p1_card == p2_card:
        if len(deck1) < 5: # If one player doesn't have enough cards for a war, that player loses
            deck2 = [1] * 52
            return deck1, deck2
        elif len(deck2) < 5:
            deck1 = [1] * 52
            return deck1, deck2
        else:
            # If war is viable, play it
            return play_turn(deck1[war_n+1:], deck2[war_n+1:], to_append + deck1[:war_n+1] + deck2[:war_n+1])
    else:
        to_append += [p1_card, p2_card]
        random.shuffle(to_append)
        if p1_card > p2_card:
            deck1 += to_append
        else:
            deck2 += to_append
    del deck1[0] # Remove played cards from decks
    del deck2[0]
    return deck1, deck2

if not read_file: # Running simulation anew
    t1 = time.time()

    for i in range(n_games):
        game_lengths.append(game(WAR_N))

    tf = time.time() - t1

    fname = f"{datetime.datetime.now().strftime('%m-%d-%Y %H%M%S')}.txt"
    f = open(fname, "w")
    f.writelines(str(game_lengths))
    print(f"The average game length on {n_games} games is {np.mean(game_lengths)} turns. Took {tf} seconds.")
else: # Reading data from previous simulation
    lengths_str = open(fname, "r").read()
    game_lengths = [int(x) for x in lengths_str[1:-1].split(", ")]

length_set = sorted(list(set(game_lengths))) # All unique game lengths from sample
counts = [game_lengths.count(x) for x in length_set] # Number of times each game length appears

plt.scatter(length_set, counts, s=[1]*len(length_set))
plt.show()