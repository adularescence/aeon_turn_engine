#!/usr/bin/env python3

# Simulates an "Aeon's End" (a board game) "Turn Order Deck"
# arg0 - the number of players

import math, random, sys

if len(sys.argv) != 2 or sys.argv[1] not in ['2', '3', '4']:
    print ("""
    Please provide the number of players to play with. The number of players must be 2, 3, or 4:
    Usage: {} <# of players>
    """.format(sys.argv[0]))
    sys.exit(2)



### GLOBAL VARS ###

player_count = int(sys.argv[1])
two_player_deck = ['Nemesis', 'Nemesis', 'Player 1', 'Player 1', 'Player 2', 'Player 2']
three_player_deck = ['Nemesis', 'Nemesis', 'Player 1', 'Player 2', 'Player 3', 'Wild']
four_player_deck = ['Nemesis', 'Nemesis', 'Player 1', 'Player 2', 'Player 3', 'Player 4']

help_key = 'h'
shuffle_key = 's'
peek_key = 'p'
discard_pile_key = 'd'
rearrange_key = 'r'
lash_nemesis_key = 'l'

help_string = """Useful keystrokes:
    h - shows this (again)
    p - peek at the top card (Flare or Garnet Shard)
    s - shuffles the discard pile into the deck
    d - shows the discard pile and number of cards remaining in the deck
    r - rearranges the deck (Xaxos's Hero Power)
    l - shuffles a discarded card back into the deck (Nemesis Power or Lash's Hero Power)
    <anything else> - draws the next card"""

deck = []
discard_pile = []
key_press = None
turn_cycles = 1

### Helper Functions ###

# shamelessly copied code
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

# checks if the given string can be cast to int
def inputted_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

# creates a string that shows the index of the elements in arr
def print_with_indices(arr):
    result = ''
    for i in range(len(arr)):
        result += '  ({})[{}]'.format(i, arr[i])
    return result

# for Flare, Garnet Shard
def peek_top():
    key_press = None

    # ensure that we want to peek at the top of the deck
    while True:
        key_press = input('Are you sure you want to peek at the next card in the deck? [y/N]\n')
        if key_press == 'y':
            break
        elif key_press in ['', 'n', 'N']:
            print('Okay, cancelling...')
            return
    
    # reveal the top of the deck, then decide if it goes back on top or to the bottom
    print('Okay, the next card in the deck is [{}]'.format(deck[-1]))
    while True:
        print('Return the [{}] card to the [t]op of the deck, or to the [b]ottom of the deck? Current discard pile:\n  [{}]'.format(deck[-1], '] ['.join(discard_pile)))
        key_press = input()
        if key_press == 't':
            # require confirmation
            print('Return the [{}] card to the top of the deck? [Y/n]'.format(deck[-1]))
            key_press = input()
            if key_press in ['', 'y', 'Y']:
                print('Okay, returning the [{}] card to the top of the deck.'.format(deck[-1]))
                return
            # else ask whether to put on top or bottom
        elif key_press == 'b':
            # require confirmation
            print('Return the [{}] card to the bottom of the deck? [Y/n]'.format(deck[-1]))
            key_press = input()
            if key_press in ['', 'y', 'Y']:
                print('Okay, returning the [{}] card to the bottom of the deck.'.format(deck[-1]))
                deck.insert(0, deck.pop())
                return
            # else ask whether to put on top or bottom
        # else ask whether to put on top or bottom

# for Xaxos's Hero Power
def rearrange_deck(deck, first_time=True):
    key_press = None

    # ensure that we want to rearrange the deck
    while first_time and True:
        print('There are {} cards left in the deck.'.format(len(deck)))
        key_press = input('Are you sure you want to rearrange the deck? [y/N]\n')
        if key_press == 'y':
            break
        elif key_press in ['', 'n', 'N']:
            print('Okay, cancelling...')
            return deck

    # copy the passed in deck, and then pick the order of the new deck one by one
    print('Rearrange the cards in the deck in the desired order of play.')
    tmp_deck = deck.copy()
    new_deck = []
    cards_returned = 1
    while len(tmp_deck) != 1:
        print('Which card should be {}? (Enter the corresponding index):'.format(ordinal(cards_returned)))
        key_press = input('  {}\n'.format(print_with_indices(tmp_deck)))
        if key_press == 'q':
            print('Restarting...')
            return rearrange_deck(deck, False)
        elif key_press in ['0', '1', '2', '3', '4', '5'][:len(tmp_deck)] and inputted_int(key_press):
            selected_card = tmp_deck.pop(int(key_press))
            new_deck.append(selected_card)
            cards_returned += 1

    # all but one cards selected, the last one just goes to the bottom
    # then we ask if this new order is correct
    # if it is good, return the new order
    # if it is bad, call itself because we have seen the order of the cards already and must finish the deed
    selected_card = tmp_deck.pop()
    new_deck.append(selected_card)
    print('Then the {} and final card shall be [{}]'.format(ordinal(cards_returned), new_deck[-1]))
    print('The new deck shall look like [{}], is this acceptable? [Y/n]'.format('] ['.join(new_deck)))
    while True:
        key_press = input()
        if key_press in ['', 'y', 'Y']:
            print('Okay the new deck looks like [{}].'.format('] ['.join(new_deck)))
            return list(reversed(new_deck))
        else:
            print('Restarting then...')
            return rearrange_deck(deck, False)
    
# for Lash's Hero Power
def return_one_card():
    key_press = None

    # ensure that we want to return one card from the discard pile
    while True:
        key_press = input('Are you sure you want to shuffle a card from the discard pile into the deck? [y/N]\n')
        if key_press == 'y':
            break
        elif key_press in ['', 'n', 'N']:
            print('Okay, cancelling...')
            return

    # prompt for which card to return, then return that card to the deck and shuffle the deck
    while True:
        print('Which of these cards would you like to shuffle back into the deck? (Enter the corresponding index):')
        key_press = input('  {}\n'.format(print_with_indices(discard_pile)))
        if key_press == 'q':
            print('Okay, cancelling...')
            return
        elif key_press in ['0', '1', '2', '3', '4', '5'][:len(discard_pile)] and inputted_int(key_press):
            selected_card = discard_pile[int(key_press)]
            key_press = input('Shuffle the [{}] card back into the deck? [Y/n]\n'.format(selected_card))
            if key_press in ['', 'y', 'Y']:
                print('Okay, shuffling the [{}] card back into the deck.'.format(selected_card))
                discard_pile.remove(selected_card)
                deck.append(selected_card)
                random.shuffle(deck)
                print('The remaining discarded cards are: [{}]'.format('] ['.join(discard_pile)))
                return



### MAIN ###

try:
    # Setup
    if player_count == 2:
        print('The number of players is {}, so the deck will contain [{}].'.format(player_count, '] ['.join(two_player_deck)))
        deck = two_player_deck.copy()
    elif player_count == 3:
        print('The number of players is {}, so the deck will contain [{}].'.format(player_count, '] ['.join(three_player_deck)))
        deck = three_player_deck.copy()
    elif player_count == 4:
        print('The number of players is {}, so the deck will contain [{}].'.format(player_count, '] ['.join(four_player_deck)))
        deck = four_player_deck.copy()
    random.shuffle(deck)
    print("This is the {} set of turns.".format(ordinal(turn_cycles)))
    print(help_string)

    # Turn Cycle
    while True:
        key_press = input()
        if key_press == help_key:
            print(help_string)
        elif key_press == shuffle_key:
            if len(deck) == 0:
                print('Shuffling the discard pile into the deck.')
                deck = discard_pile
                random.shuffle(deck)
                discard_pile = []
                turn_cycles += 1
                print("This is the {} set of turns.".format(ordinal(turn_cycles)))
            else:
                print('Ignoring because the deck needs to be exhausted before you can shuffle it.')
        elif key_press == peek_key:
            if len(deck) == 0:
                print('Ignoring because the deck has no cards left to peek at.')
            else:
                peek_top()
        elif key_press == discard_pile_key:
            print('The discarded cards are: [{}]'.format('] ['.join(discard_pile)))
            print('There are {} cards left in the deck.'.format(len(deck)))
        elif key_press == rearrange_key:
            if len(deck) == 1:
                print('Ignoring because the deck only has one card left to rearrange.')
            elif len(deck) == 0:
                print('Ignoring because the deck has no cards left to rearrange.')
            else:
                deck = rearrange_deck(deck)
        elif key_press == lash_nemesis_key:
            if len(discard_pile) == 0:
                print('Ignoring because the discard pile has no cards to shuffle back into the deck.')
            else:
                return_one_card()
        else:
            if len(deck) != 0:
                discard_pile.append(deck.pop())
                print('The next turn belongs to: [{}]'.format(discard_pile[-1]))
            else:
                print('Cannot draw because the deck has been exhausted.')
except (EOFError, KeyboardInterrupt) as e:
    print("""
    So you've pressed Ctrl+C or Ctrl+D.

    Fortunately I have saved the state of the deck, just for you:
      [{}]
    And the discard pile:
      [{}]
    """.format('] ['.join(list(reversed(deck))), '] ['.join(discard_pile)))
    exit(-1)
