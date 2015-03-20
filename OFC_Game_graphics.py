#!/usr/bin/env python3.4

from random import shuffle, randrange
from tkinter import *
from PIL import Image, ImageTk



# Height and width of the Tk window
HEIGHT = 550
WIDTH = 1024

# A collection of all cards in a deck from which to crop each individual card image
CARDS = Image.open("card_images.png") 
CARD_HEIGHT = 98
CARD_WIDTH = 74

# These lists represent where the large board (for the current player) should be displayed on the canvas
DEALT_GRAPHICS = [[WIDTH/2 + (2*i - 1)/2 * CARD_WIDTH + (4*i - 1) * 3, HEIGHT - 5 - CARD_HEIGHT - 3,
                   WIDTH/2 + (2*i + 1)/2 * CARD_WIDTH + (4*i + 1) * 3, HEIGHT - 5 + 3]
                   for i in range(-2, 3)]
BACK_GRAPHICS  = [[WIDTH/2 + (2*i - 1)/2 * CARD_WIDTH + (4*i - 1) * 3, HEIGHT - 60 - CARD_HEIGHT/2 - 1 * (CARD_HEIGHT + 12) - 3,
                   WIDTH/2 + (2*i + 1)/2 * CARD_WIDTH + (4*i + 1) * 3, HEIGHT - 60 + CARD_HEIGHT/2 - 1 * (CARD_HEIGHT + 12) + 3]
                   for i in range(-2, 3)]
MID_GRAPHICS   = [[WIDTH/2 + (2*i - 1)/2 * CARD_WIDTH + (4*i - 1) * 3, HEIGHT - 60 - CARD_HEIGHT/2 - 2 * (CARD_HEIGHT + 12) - 3,
                   WIDTH/2 + (2*i + 1)/2 * CARD_WIDTH + (4*i + 1) * 3, HEIGHT - 60 + CARD_HEIGHT/2 - 2 * (CARD_HEIGHT + 12) + 3]
                   for i in range(-2, 3)]
FRONT_GRAPHICS = [[WIDTH/2 + (2*i - 1)/2 * CARD_WIDTH + (4*i - 1) * 3, HEIGHT - 60 - CARD_HEIGHT/2 - 3 * (CARD_HEIGHT + 12) - 3,
                   WIDTH/2 + (2*i + 1)/2 * CARD_WIDTH + (4*i + 1) * 3, HEIGHT - 60 + CARD_HEIGHT/2 - 3 * (CARD_HEIGHT + 12) + 3]
                   for i in range(-1, 2)]

# Together with GRAPHICS_SMALL_OFFSETS, these lists represent where the small boards should be displayed in the canvas
BACK_GRAPHICS_SMALL  = [[WIDTH/2 + ((2*i - 1)/2 * CARD_WIDTH + (4*i - 1) * 3)/2, (HEIGHT - 60 - CARD_HEIGHT/2 - 1 * (CARD_HEIGHT + 12) - 3)/2,
                         WIDTH/2 + ((2*i + 1)/2 * CARD_WIDTH + (4*i + 1) * 3)/2, (HEIGHT - 60 + CARD_HEIGHT/2 - 1 * (CARD_HEIGHT + 12) + 3)/2]
                         for i in range(-2, 3)]
MID_GRAPHICS_SMALL   = [[WIDTH/2 + ((2*i - 1)/2 * CARD_WIDTH + (4*i - 1) * 3)/2, (HEIGHT - 60 - CARD_HEIGHT/2 - 2 * (CARD_HEIGHT + 12) - 3)/2,
                         WIDTH/2 + ((2*i + 1)/2 * CARD_WIDTH + (4*i + 1) * 3)/2, (HEIGHT - 60 + CARD_HEIGHT/2 - 2 * (CARD_HEIGHT + 12) + 3)/2]
                         for i in range(-2, 3)]
FRONT_GRAPHICS_SMALL = [[WIDTH/2 + ((2*i - 1)/2 * CARD_WIDTH + (4*i - 1) * 3)/2, (HEIGHT - 60 - CARD_HEIGHT/2 - 3 * (CARD_HEIGHT + 12) - 3)/2,
                         WIDTH/2 + ((2*i + 1)/2 * CARD_WIDTH + (4*i + 1) * 3)/2, (HEIGHT - 60 + CARD_HEIGHT/2 - 3 * (CARD_HEIGHT + 12) + 3)/2]
                         for i in range(-1, 2)]

GRAPHICS_SMALL_OFFSETS = [[-3*WIDTH/8, -HEIGHT/10 + 30], [-3*WIDTH/8, HEIGHT/2], [3*WIDTH/8, -HEIGHT/10 + 30], [3*WIDTH/8, HEIGHT/2]]



def cmp_ranks(card_list1, card_list2):
    # This function takes two ordered lists of cards and compares them element by element.
    # A list of cards is ordered if it is sorted by number of occurances of each rank
    # and then by rank.

    # Adding 12 and modding by 13 makes 1 -> 12, 2 -> 0, ..., 13 -> 11
    # as in 2, 3, ..., 10, J, Q, K, A.
    for i in range(min(len(card_list1), len(card_list2))):
        if ((card_list1[i] + 11) % 13) < ((card_list2[i] + 11) % 13):
            return -1
        elif ((card_list1[i] + 11) % 13) > ((card_list2[i] + 11) % 13):
            return 1
    if len(card_list1) < len(card_list2):
        return -1
    elif len(card_list1) > len(card_list2):
        return 1
    else:
        return 0



class Card(object):
    # The Card class represents each playing card found in Game.deck.
    # It stores information such as the small and regular images corresponding to the card's rank and suit, 
    # as well as their position on the Game's canvas

    def __init__(self, rank, suit):
        # If the rank and suit of the card are in the correct ranges, set self.rank and self.suit
        if not isinstance(rank, int):
            print("\nRank of new Card is not an integer.\n\n")
            raise ValueError
        if rank > 13 or rank < 1:
            print("\nRank of new Card is out of range.\n\n")
            raise ValueError
        if suit not in ['c','s','h','d']:
            print("\nInvalid Suit {}.\n\n".format(suit))
            raise ValueError

        self.rank = rank
        self.suit = suit

        # Find where to crop CARDS to get the correct image for the card
        global CARDS, CARD_WIDTH, CARD_HEIGHT
        suit_num = ['c','s','h','d'].index(self.suit)
        box = [(self.rank - 1) * (CARD_WIDTH - 1), suit_num * CARD_HEIGHT,
               self.rank * (CARD_WIDTH - 1) + 1, (suit_num + 1) * CARD_HEIGHT]

        # Create a regular image for display on the main board and a small image for display on the small boards
        self.image = ImageTk.PhotoImage(CARDS.crop(box))
        self.position = None
        self.corners = None

        self.image_small = ImageTk.PhotoImage(CARDS.crop(box).resize((int(CARD_WIDTH/2), int(CARD_HEIGHT/2)), Image.ANTIALIAS))
        self.position_small = None
        self.corners_small = None

        # Makes it easier to move the card using Game.move_card()
        self.is_in_hand = [] # [Index of hand, Index of card in hand]


    # __str__() and __repr__() are defined in a natural way to allow for displaying the card in the terminal
    def __str__(self):
        if self.rank == 1:
            return('A' + self.suit)
        elif self.rank == 10:
            return('T' + self.suit)
        elif self.rank == 11:
            return('J' + self.suit)
        elif self.rank == 12:
            return('Q' + self.suit)
        elif self.rank == 13:
            return('K' + self.suit)
        else:
            return(str(self.rank) + self.suit)

    def __repr__(self):
        return(str(self))



class Player:
    """
    # The Player class represents a human player character.
    # It stores the player's name, hands, and cumulative score, and has the ability to score
    # each of the player's hands. This is used by Game.score_round to score each round.
    """

    def __init__(self, name):
        # Store the name of the player and initialize their (empty) hands

        self.name = str(name)

        self.back = 5 * [None]
        self.mid = 5 * [None]
        self.front = 3 * [None]
        self.all_hands = [self.back, self.mid, self.front]

        # Current hand scores (used by Game.score_round())
        self.back_score = 0
        self.mid_score = 0
        self.front_score = 0

        self.total_score = 0


    def greet(self):
        # Greet the player by name
        print("Welcome, {}!\n".format(self.name))


    def hand_score(self, hand):
        """
        # Go through each possible hand type in order of strength and stop when the given hand matches
        # that strength. Return a list of the hand type, as well as an ordered hand (for use in cmp_ranks())
        # by Game.score_round().
        """

        # Compile list of 5 consecutive integers to represent straights
        straightranges = [set(range(i, i + 5)) for i in range(1, 10)]
        straightranges.append(set([10, 11, 12, 13, 1]))     # Can also have 10 J Q K A

        is_flush = 0
        is_straight = 0

        ranks = [card.rank for card in hand]
        suits = [card.suit for card in hand]

        # Sets get rid of repeats, which is useful for checking hand type
        set_r = set(ranks)
        set_s = set(suits)

        # Sort first by rank (descending), then by number of occurences (descending)
        ranks = sorted(
            sorted(ranks, key = lambda r: (r + 11) % 13, reverse = True)
            , key = lambda r: ranks.count(r), reverse = True)

        if len(hand) == 5:
            if len(set_s) == 1:
                is_flush = 1
            if set_r in straightranges:
                is_straight = 1


            if is_straight + is_flush == 2:
                # At least a straight flush
                if set_r == set([1, 10, 11, 12, 13]):
                    return [9, ranks]
                else:
                    return [8, ranks]
                
            elif len(set_r) == 2:
                # At least a full house
                if ranks.count(ranks[0]) in [1, 4]:
                    return [7, ranks]
                else:
                    return [6, ranks]
                
            # At this point, the hand is at most a flush
            elif is_flush == 1:
                return [5, ranks]
                
            elif is_straight == 1:
                return [4, ranks]
                
            elif len(set_r) == 3:
                if any([ranks.count(ranks[i]) == 3 for i in range(3)]):
                    return [3, ranks]
                else:
                    return [2, ranks]
                
            elif len(set_r) == 4:
                # Not all ranks are distinct
                return [1, ranks]
                
            else:
                # All ranks are distinct
                return [0, ranks]

        elif len(hand) == 3:
            if len(set_r) == 1: # 3 of a kind
                return [3, ranks]
            elif len(set_r) == 2: # one pai
                return [1, ranks]
            else: # high card
                return [0, ranks]

        else:
            print("\nInvalid hand size {}.\n\n".format(len(hand)))
            raise ValueError



class Game:
    """
    # The is the main class of the program and represents the current game itself.
    # It stores all the relevant information for running the game (such as a list of players and turn and round numbers)
    # and scoring the game (such as self.royalties_[fmb]). It also importantly controls the graphics output, since
    # self.root = Tk() is one of its attributes and all graphics are attached to self.root.
    #
    # Overview of Major Functions:
    # - self.turn(player, num_cards), self.goto_next_turn() work together to let each player play their turn, and
    # act as a sort of main loop for the game. self.turn displays the current player's hands on the main board
    # using self.show_hands(current_player) and deals num_cards cards to self.current_player for use on their turn. Then
    # the turn "begins" and lasts until all cards that have been dealt have been placed into the current player's hand.
    # When self.end_turn_button is activated, the game checks that the turn has been completed using self.goto_next_turn(),
    # and if it has been, it moves all the cards from the main board to the current player's small board. It then checks
    # if the round is over, and if so, goes to the next round. Otherwise, self.turn is called for the next player.
    # - self.new_round() is called when a new round has to begin. It empties each player's hand and clears each player's
    # small board. It then sets self.dealer to the player after self.dealer and self.current_player to the player after
    # self.dealer. It then begins the new round by calling self.turn for self.current_player.
    # - self.draw_card(card, position) takes a Card object and draws it in self.canvas at position
    # - self.move_card(event) is called whenever the left mouse button is clicked. It selects a card on the canvas on
    # the first click and moves it to the position of the second click if the position is valid.
    # - self.play_game() draws the main board and small boards for each player onto self.canvas and then starts the first
    # round of the game using self.new_round().
    """

    def __init__(self):
    ### ----------------------------- Graphics ----------------------------- ###
        # Store all graphics within the Game class using self.root
        self.root = Tk()

        # A label that displays information whenever necessary (such as the current player
        # or the score at the end of a round)
        self.current_message = "Welcome to OFC!"
        self.current_message_label = Label(self.root, text = self.current_message)
        self.current_message_label.grid(row = 0, column = 1)

        # The canvas to draw all the images onto
        self.canvas = Canvas(self.root, height = HEIGHT, width = WIDTH)
        self.canvas.grid(row = 1, column = 0, rowspan = 1, columnspan = 3)
        self.canvas["bg"] = "dark green"

        # Clicks on the canvas will call self.move_card to attempt to move a dealt card
        self.canvas.bind("<Button-1>", self.move_card)

        # Button to click after all the dealt cards have been placed to proceed to the next turn
        self.end_turn_button = Button(self.root, text = "End Turn!", width = 10, command = lambda: self.goto_next_turn())
        self.end_turn_button.grid(row = 2, column = 1)

        # Start a new game
        self.new_game_button = Button(self.root, text = "New Game!", width = 10, command = lambda: self.new_game())
        self.new_game_button.grid(row = 2, column = 0)

        # Start a game that is almost finished and is quite unfair (for demonstration purposes)
        self.almost_done_game_button = Button(self.root, text = "I'm so good.", width = 10, command = lambda: self.almost_done_game())
        self.almost_done_game_button.grid(row = 2, column = 2)

        # Keep track of all the cards that have been drawn for easier deletion. The key is the card
        # object and the value is the output of the self.canvas.create_image method.
        self.cards_on_canvas = dict()
        self.cards_on_canvas_small = dict()

        # Keep track of the lists that represent the positions of the boxes that make up each player's small board
        self.small_boards = []

    ### ---------------------------- Turn/Round ---------------------------- ###

        # First turn has 5 cards dealt, next 8 turns have 1 card each
        self.round_number = 0
        self.turn_number = 0
        self.max_turns = 9

        # Will be created by self.new_deck()
        self.deck = None
        # The cards that can be moved around on the current turn (could be named self.dealt_cards)
        self.unlocked_cards = []
        # The cards that were dealt this turn and have not been placed into a hand yet
        self.unplaced_cards = []
        # The card that self.move_card() will move on the next click
        self.card_to_move = None

    ### ----------------------------- Scoring ------------------------------ ###

        # Royalties are additional points awarded to players who build hands of a certain strength without
        # busting. They must be accounted for during scoring.

        # Build dictionary of royalties for front hands. The key is a string representing hand strength and
        # the rank of the relevant cards. Since there are only 3 cards, there are not many possible hands,
        # so only single pairs and three of a kinds need to be considered. Thus, the hand strength along with
        # the first rank in the ordered ranks is enough to determine the royalty entirely.
        self.royalties_f = dict()
        for i in range(1, 14):
            self.royalties_f["0 " + str(i)] = 0
        for i in range(2, 6):
            self.royalties_f["1 " + str(i)] = 0
        for i in range(6, 14):
            self.royalties_f["1 " + str(i)] = i - 5
        self.royalties_f["1 1"] = 9
        for i in range(1, 14):
            self.royalties_f["3 " + str(i)] = i + 9
        # Build dictionary of royalties for middle and back hands. Royalties for the middle and back hands are
        # simpler than those for front hands and depend solely on hand strength.
        self.royalties_m = {0: 0, 1: 0, 2: 0, 3: 2, 4: 4, 5: 8, 6: 12, 7: 20, 8: 30, 9: 50}
        self.royalties_b = {0: 0, 1: 0, 2: 0, 3: 0, 4: 2, 5: 4, 6: 6, 7: 10, 8: 15, 9: 25}

    ### ----------------------------- Players ------------------------------ ###

        # Find the number of players and construct a list of players
        num_players = input("Welcome to OFC! How many people will be playing? (2 - 4) ")
        while num_players not in ["2","3","4"]:
            print("Invalid selection.")
            num_players = input("How many people will be playing? (2 - 4) ")
        num_players = int(num_players)

        self.players = []
        for i in range(num_players):
            while True:
                name = input("Player {}, what is your name?\n".format(i))
                if name not in [self.players[i].name for i in range(len(self.players))]:
                    break
                else:
                    print("The name \"{}\" has already been taken!".format(name))
            new_player = Player(name)
            self.players.append(new_player)
            new_player.greet()

        # Will be set in self.new_round()
        self.dealer = None
        self.current_player = None


    def draw_card(self, card, position = (0, 0)):
        """
        # Draw a card to a position on the canvas
        """

        global CARD_WIDTH, CARD_HEIGHT
        # Store the position and coordinates of the corners of the card
        card.position = position
        card.corners = [card.position[0] - CARD_WIDTH / 2 + 2, card.position[1] - CARD_HEIGHT / 2 + 2,
                        card.position[0] + CARD_WIDTH / 2, card.position[1] + CARD_HEIGHT / 2]

        # Store the ID of the image given by self.canvas.create_image in a dictionary for easier deletion
        # and create the image
        self.cards_on_canvas[card] = self.canvas.create_image(card.position, image = card.image)


    def draw_card_small(self, card, position = (0, 0)):
        """
        # Draw a card to a position on the canvas, using its small image
        """

        global CARD_WIDTH, CARD_HEIGHT
        card.position_small = position
        card.corners_small = [card.position_small[0] - CARD_WIDTH / 4 + 1, card.position_small[1] - CARD_HEIGHT / 4 + 1,
                              card.position_small[0] + CARD_WIDTH / 4, card.position_small[1] + CARD_HEIGHT / 4]
        self.cards_on_canvas_small[card] = self.canvas.create_image(card.position_small, image = card.image_small)


    def deal(self, num_cards):
        """
        # Draw the top num_cards cards of self.deck to the main board for use on self.current_player's turn
        """

        # Check that a turn is not currently in progress (this is unnecessary, but just in case)
        if self.unplaced_cards != []:
            print("\nThe previous turn is not over.\n")
            return None

        # Check that the number of cards to deal is not too high (5 is the maximum)
        if num_cards > 5:
            print("\nCannot deal {} cards (maximum is 5).\n".format(num_cards))
            num_cards = 5

        # Check that there are enough cards left in the deck
        if len(self.deck) < num_cards:
            print("\nCannot deal {} cards. Only {} left in the deck.\n".format(num_cards, len(self.deck)))
            num_cards = len(self.deck)

        # Draw the cards to the boxes defined by DEALT_GRAPHICS and add them to the list of manipulable cards
        # for the next turn
        i = 0
        while i < num_cards:
            global DEALT_GRAPHICS
            dims = DEALT_GRAPHICS[i]

            card = self.deck.pop()

            self.draw_card(card, ((dims[0] + dims[2])/2, (dims[1] + dims[3])/2))
            self.unlocked_cards.append(card)
            self.unplaced_cards.append(card)

            i += 1


    def show_hands(self, player):
        """
        # Draw the back, middle, and front hands of a player to the main board to indicate it is their turn
        # and allow for easier placement of dealt cards into hands.
        """

        global BACK_GRAPHICS, MID_GRAPHICS, FRONT_GRAPHICS
        lists_of_graphics = [BACK_GRAPHICS, MID_GRAPHICS, FRONT_GRAPHICS]

        i = 0
        while i < len(player.all_hands):
            # Draw the cards in player.**** to the boxes defined by ****_GRAPHICS
            hand = player.all_hands[i]
            j = 0
            while j < len(hand):
                card = hand[j]
                if card != None:
                    dims = lists_of_graphics[i][j]
                    self.draw_card(card, ((dims[0] + dims[2])/2, (dims[1] + dims[3])/2))
                j += 1
            i += 1


    def turn(self, player, num_cards):
        """
        # Deal the necessary number of cards to self.current_player and draw self.current_player's hands on the main board.
        # The program will let the player move unlocked cards at will but will do nothing until self.end_turn_button is
        # activated.
        """

        self.current_player = player # Just in case

        if self.current_player not in self.players: # Just in case
            print("\nPlayer is not in game.\n")
            raise IndexError

        # Update self.current_message_label to indicate it is self.current_player's turn
        if self.current_message_label != None:
            self.current_message_label.destroy()
        self.current_message = "It is " + self.current_player.name + "\'s turn."
        self.current_message_label = Label(self.root, text = self.current_message)
        self.current_message_label.grid(row = 0, column = 1)

        print("{}, it is your turn.".format(player.name))

        self.deal(num_cards)
        self.show_hands(player)


    def goto_next_turn(self):
        """
        # Called whenever self.end_turn_button is pressed. Checks that all dealt cards have been placed
        # and, if so, goes to either the next turn if the current round is not over or to the next round
        # if the current round is over.
        """

        if self.unplaced_cards != []:
            print("\nNot all cards have been placed yet!\n")
        else:
            self.unlocked_cards = [] # Lock all unlocked cards

            # Clear the main board of the previous player's cards and draw them onto the correct small board
            small_board = self.small_boards[self.players.index(self.current_player)]
            i = 0
            while i < len(self.current_player.all_hands):
                hand = self.current_player.all_hands[i]

                j = 0
                while j < len(hand):
                    card = hand[j]

                    if card != None:
                        # Remove the card from the canvas and from self.cards_on_canvas
                        self.canvas.delete(self.cards_on_canvas[card])
                        self.cards_on_canvas.pop(card)

                        # Draw the card onto self.current_player's small board in the position corresponding
                        # to its place in self.current_player's hands
                        if card.position_small == None:
                            dims = small_board[i][j]
                            self.draw_card_small(card, ((dims[0] + dims[2])/2, (dims[1] + dims[3])/2))
                    j += 1
                i += 1

            if self.current_player == self.dealer:
                self.turn_number += 1 # Dealer plays last

            # Set self.current_player to be the next player (go to the first player if the current player
            # is the last player)
            new_index = (self.players.index(self.current_player) + 1) % len(self.players)
            self.current_player = self.players[new_index]

            # If the round is over, go to the next round
            if self.turn_number >= self.max_turns:
                # Display score
                self.score_round()
                # Pressing any key at this point will proceed to the next round
                self.root.bind("<Key>", self.goto_next_round)
                print("\nPress any key to continue.\n")
            # Otherwise, go to the next turn
            else:
                if self.turn_number == 0:
                    self.turn(self.current_player, 5)
                else:
                    self.turn(self.current_player, 1)


    def goto_next_round(self, event):
        """
        # Go to the next round if the game is not over. Otherwise, score the game.
        """

        # <Key> should only be bound while the score is being displayed.
        self.root.unbind("<Key>")

        self.round_number += 1
        if self.round_number >= len(self.players):
            self.score_game()
        else:
            self.new_round()


    def new_round(self):
        """
        # Begin a new round by clearing the small boards (the main board will have been cleared by self.goto_next_turn),
        # creating a new deck, clearing each player's hand, and shifting self.dealer to the player after self.dealer, and
        # then beginning the first turn.
        """

        # Clear the small boards
        for card_small in self.cards_on_canvas_small.keys():
            self.canvas.delete(card_small)
        self.cards_on_canvas_small.clear()

        # Create a fresh deck
        self.deck = self.new_deck()
        # Clear each player's hand
        for player in self.players:
            player.back = 5 * [None]
            player.mid = 5 * [None]
            player.front = 3 * [None]
            player.all_hands = [player.back, player.mid, player.front]

        # Set the dealer
        if self.dealer == None:
            self.dealer = self.players[0]
        else:    
            new_index = (self.players.index(self.dealer) + 1) % len(self.players)
            self.dealer = self.players[new_index]

        print("\nBeginning round {}. {} is the dealer.\n".format(self.round_number, self.dealer.name))

        self.turn_number = 0
        # The first player is the player after the dealer.
        new_index = (self.players.index(self.dealer) + 1) % len(self.players)
        self.current_player = self.players[new_index]
        # The first turn deals 5 cards
        self.turn(self.current_player, 5)


    def score_round(self):
        """
        # Score the round. Take into account players who have busted (their hands are not increasing in strength)
        # and the royalties awarded to each player who has not busted.
        """

        self.round_royalties = len(self.players) * [0]
        self.round_hand_scores = len(self.players) * [0]

        # Score each player's hands
        for player in self.players:
            player.front_score = player.hand_score(player.front)
            player.mid_score = player.hand_score(player.mid)
            player.back_score = player.hand_score(player.back)

        # Find which players have busted
        busted = len(self.players) * [0]
        i = 0
        while i < len(busted):
            if self.players[i].front_score[0] > self.players[i].mid_score[0]:
                busted[i] = 1
                print("{} busted! (front >> mid)".format(self.players[i].name))
            elif self.players[i].front_score[0] == self.players[i].mid_score[0]:
                if cmp_ranks(self.players[i].front_score[1], self.players[i].mid_score[1]) == 1:
                    busted[i] = 1
                    print("{} busted! (front => mid)".format(self.players[i].name))

            if self.players[i].mid_score[0] > self.players[i].back_score[0]:
                busted[i] = 1
                print("{} busted! (mid >> back)".format(self.players[i].name))
            elif self.players[i].mid_score[0] == self.players[i].back_score[0]:
                if cmp_ranks(self.players[i].mid_score[1], self.players[i].back_score[1]) == 1:
                    busted[i] = 1
                    print("{} busted! (mid => back)".format(self.players[i].name))

            i += 1

        # Add royalties to score
        i = 0
        while i < len(busted):
            if busted[i] == 0:
                # player.[front, mid, back]_score is of the form [strength, ordered_ranks]
                self.round_royalties[i] += self.royalties_b[self.players[i].back_score[0]]
                self.round_royalties[i] += self.royalties_m[self.players[i].mid_score[0]]
                self.round_royalties[i] += self.royalties_f[
                    str(self.players[i].front_score[0]) + ' ' + str(self.players[i].front_score[1][0])
                    ]
            i += 1

        # Score each player relative to each other player
        relative_scores_message = ""
        i = 0
        while i < len(self.players) - 1:
            j = i + 1
            while j < len(self.players):
                current_score = 0

                # Busting is equivalent to getting swept (but with no royalties)
                if busted[i] == 1 or busted[j] == 1:
                    if busted[i] == 1:
                        current_score += -6
                    if busted[j] == 1:
                        current_score += 6

                else:
                    # Compare corresponding hands and give a point to the player with the stronger hand

                    if self.players[i].front_score[0] < self.players[j].front_score[0]:
                        current_score += -1
                    elif self.players[i].front_score[0] == self.players[j].front_score[0]:
                        # Look through the ranks element by element to see who wins the tie
                        current_score += cmp_ranks(self.players[i].front_score[1], self.players[j].front_score[1])
                    else:
                        current_score += 1

                    if self.players[i].mid_score[0] < self.players[j].mid_score[0]:
                        current_score += -1
                    elif self.players[i].mid_score[0] == self.players[j].mid_score[0]:
                        current_score += cmp_ranks(self.players[i].mid_score[1], self.players[j].mid_score[1])
                    else:
                        current_score += 1

                    if self.players[i].back_score[0] < self.players[j].back_score[0]:
                        current_score += -1
                    elif self.players[i].back_score[0] == self.players[j].back_score[0]:
                        current_score += cmp_ranks(self.players[i].back_score[1], self.players[j].back_score[1])
                    else:
                        current_score += 1

                    if current_score == 3 or current_score == -3:
                        # Sweep, so score is doubled
                        current_score *= 2

                # The current_score variable represents self.players[i]'s score against self.players[j], so
                # will be positive if i "wins" and negative if j "wins"
                self.round_hand_scores[i] += current_score
                self.round_hand_scores[j] += -current_score
                self.players[i].total_score += self.round_royalties[i] - self.round_royalties[j]
                self.players[j].total_score += self.round_royalties[j] - self.round_royalties[i]

                print("{} vs. {}: {}".format(self.players[i].name, self.players[j].name, current_score))
                relative_scores_message += "{} vs. {}: {}".format(self.players[i].name, self.players[j].name, current_score)
                if j == len(self.players) - 1 and i == len(self.players) - 2:
                        relative_scores_message += '\n'
                else:
                    relative_scores_message += ", "

                j += 1
            i += 1

        # Create a message listing royalties for each player for display in self.current_message_label.
        # Also print similar information to the terminal.
        royalty_scores_message = "Royalties: "
        i = 0
        while i < len(self.players):
            player = self.players[i]
            print("{} had {} points in royalties this round.".format(player.name, self.round_royalties[i]))

            royalty_scores_message += "{} = {}".format(player.name, self.round_royalties[i])
            if i < len(self.players) - 1:
                royalty_scores_message += ", "
            else:
                royalty_scores_message += '\n'

            i += 1
        print()

        # Create a message listing total scores for each player for display in self.current_message_label.
        # Also print similar information to the terminal.
        total_scores_message = "Totals: "
        i = 0
        while i < len(self.players):
            player = self.players[i]
            player.total_score += self.round_hand_scores[i]
            print("{} now has a total score of {}.".format(
                player.name, player.total_score
                ))

            total_scores_message += "{} = {}".format(player.name, player.total_score)
            if i < len(self.players) - 1:
                total_scores_message += ", "
            else:
                total_scores_message += '\n'

            i += 1

        # Display self.current_message_label, which lists scoring information, and tell the user to press any key
        # to continue (in self.goto_next_turn, <Key> was bound in self.root to self.goto_next_round)
        if self.current_message_label != None:
            self.current_message_label.destroy()
        self.current_message = relative_scores_message + royalty_scores_message + total_scores_message + "Press any key to continue."
        self.current_message_label = Label(self.root, text = self.current_message)
        self.current_message_label.grid(row = 0, column = 1)


    def score_game(self):
        """
        # Display the winner both in the Terminal and in self.current_message_label
        """

        print("{} is the winner. Congratulations!\nThanks for playing!\n".format(
            sorted(self.players, key = lambda p: p.total_score, reverse = True)[0].name
            ))

        if self.current_message_label != None:
            self.current_message_label.destroy()
        self.current_message =  "{} is the winner. Congratulations!\nThanks for playing!".format(
            sorted(self.players, key = lambda p: p.total_score, reverse = True)[0].name
            )
        self.current_message_label = Label(self.root, text = self.current_message)
        self.current_message_label.grid(row = 0, column = 1)


    def new_deck(self): 
        """
        # Return a standard shuffled deck with 52 cards.
        """

        deck = [Card(i, j) for j in ['s','d','c','h'] for i in range(1, 14)]
        shuffle(deck)
        return deck


    def move_card(self, event):
        """
        # This function is meant to be called whenever the left mouse button (<Button-1>) is pressed.
        # It checks if there is a card currently queued to move (stored in self.card_to_move). If there is no queued card,
        # it checks if the mouse click is within the bounds of any newly-dealt card's image. If so, it sets that card as the
        # queued card. 
        # If there is a queued card, it checks if the mouse click was within any of the bounds defined by 
        # [BACK, MID, FRONT]_GRAPHICS, and if it is, it draws the selected card in that position after deleting its image from its
        # previous position. In any case, it sets self.card_to_move = None.
        """

        # If no card is currently selected, try to select one of the unlocked ones
        if self.card_to_move == None:
            for card in self.unlocked_cards:
                if card.corners[0] <= event.x and event.x <= card.corners[2] and card.corners[1] <= event.y and event.y <= card.corners[3]:
                        self.card_to_move = card
                        break

        # If there is already a selected card, read the click as a destination for it
        else:
            card = self.card_to_move

            global BACK_GRAPHICS, MID_GRAPHICS, FRONT_GRAPHICS
            lists_of_graphics = [BACK_GRAPHICS, MID_GRAPHICS, FRONT_GRAPHICS]
            for list_of_dims in lists_of_graphics:
                for dims in list_of_dims:
                    # Check if the click is within the bounds of an empty space in the current player's hand
                    if dims[0] <= event.x and event.x <= dims[2] and dims[1] <= event.y and event.y <= dims[3]:
                        index_of_hand = lists_of_graphics.index(list_of_dims)
                        hand = self.current_player.all_hands[index_of_hand]
                        index_to_place = list_of_dims.index(dims)

                        # If it is, check if the desired position is empty
                        if hand[index_to_place] == None:
                            # If it is...

                            # Place the card in the corresponding position in the player's hands
                            hand[index_to_place] = card

                            # If the card had already been placed temporarily somewhere this turn, remove it from
                            # its previous position in the player's hands
                            if card.is_in_hand != []:
                                self.current_player.all_hands[card.is_in_hand[0]][card.is_in_hand[1]] = None
                            card.is_in_hand = [index_of_hand, index_to_place]

                            # Delete the card from the canvas draw it again in its new position
                            self.canvas.delete(self.cards_on_canvas[card])
                            self.cards_on_canvas.pop(card)
                            card.position = None
                            card.corners = None
                            self.draw_card(card, ((dims[0] + dims[2])/2, (dims[1] + dims[3])/2))
                            
                            # The card has now been placed
                            if card in self.unplaced_cards:
                                self.unplaced_cards.remove(card)

                            self.card_to_move = None
                            return(card)
            self.card_to_move = None


    def play_game(self):
        """
        # Draw the main board and small boards for each player and begin the game by starting a new round
        """

        global DEALT_GRAPHICS, BACK_GRAPHICS, MID_GRAPHICS, FRONT_GRAPHICS
        global BACK_GRAPHICS_SMALL, MID_GRAPHICS_SMALL, FRONT_GRAPHICS_SMALL
        global GRAPHICS_SMALL_OFFSETS

        # Draw the main board
        for list_of_graphics in [DEALT_GRAPHICS, BACK_GRAPHICS, MID_GRAPHICS, FRONT_GRAPHICS]:
            if list_of_graphics == DEALT_GRAPHICS:
                for dims in list_of_graphics:
                    self.canvas.create_rectangle(dims, fill = "light green")
            else:
                for dims in list_of_graphics:
                    self.canvas.create_rectangle(dims, fill = "green")

        # Draw each small board
        i = 0
        while i < len(self.players):
            new_small_board = []
            for list_of_graphics in [BACK_GRAPHICS_SMALL, MID_GRAPHICS_SMALL, FRONT_GRAPHICS_SMALL]:
                new_small_row = []
                for dims in list_of_graphics:
                    offset_dims = [dims[0] + GRAPHICS_SMALL_OFFSETS[i][0], dims[1] + GRAPHICS_SMALL_OFFSETS[i][1],
                                   dims[2] + GRAPHICS_SMALL_OFFSETS[i][0], dims[3] + GRAPHICS_SMALL_OFFSETS[i][1]]
                    new_small_row.append(offset_dims)
                    self.canvas.create_rectangle(offset_dims, fill = "green")
                new_small_board.append(new_small_row)
            # Store the small board's position information
            self.small_boards.append(new_small_board)

            i += 1

        self.new_round()


    def new_game(self):
        """
        # Begin an entirely new game
        """

        # Delete all existing on-screen information

        self.canvas.delete(ALL)
        if self.current_message_label != None:
            self.current_message_label.destroy()
        self.small_boards = []

        for card in self.cards_on_canvas:
            card.position = None
            card.corners = None
        self.cards_on_canvas.clear()

        for card in self.cards_on_canvas_small:
            card.position_small = None
            card.corners_small = None
        self.cards_on_canvas_small.clear()

        self.root.destroy()

        print("\n\n\nStarting a new game.\n")

        # Start a new game
        self.__init__()
        self.play_game()


    def almost_done_game(self):
        """
        # Enter a game that has been played almost to completion (intended for demonstration purposes).
        # Sotiri will have three of a kind 9s and two royal flushes at the end, while Noob will bust.
        """

        self.canvas.delete(ALL)
        if self.current_message_label != None:
            self.current_message_label.destroy()
        self.small_boards = []

        for card in self.cards_on_canvas:
            card.position = None
            card.corners = None
        self.cards_on_canvas.clear()

        for card in self.cards_on_canvas_small:
            card.position_small = None
            card.corners_small = None
        self.cards_on_canvas_small.clear()

        print("\n\n\nStarting a really fair game.\n")

        self.deck = []
        self.deck.append(Card(1, 's'))
        self.deck.append(Card(12, 'c'))
        self.deck.append(Card(1, 'h'))

        self.unlocked_cards = []
        self.unplaced_cards = []
        self.card_to_move = None

        self.round_number = 1
        self.turn_number = 7
        self.max_turns = 9

        self.players = [Player("Sotiri"), Player("Noob")]
        self.players[0].total_score = 72
        self.players[1].total_score = -72

        self.dealer = self.players[0]
        self.current_player = self.dealer

        self.players[0].front = [Card(9, 'h'), Card(9, 'd'), Card(9, 's')]
        self.players[0].mid = [Card(10, 'h'), Card(11, 'h'), Card(12, 'h'), Card(13, 'h'), None]
        self.players[0].back = [Card(10, 's'), Card(11, 's'), Card(12, 's'), Card(13, 's'), None]
        self.players[0].all_hands = [self.players[0].back, self.players[0].mid, self.players[0].front]

        self.players[1].front = [Card(2, 'h'), Card(3, 'd'), Card(4, 'c')]
        self.players[1].mid = [Card(2, 'c'), Card(4, 's'), Card(11, 's'), Card(12, 'd'), Card(8, 'h')]
        self.players[1].back = [Card(3, 's'), Card(7, 'd'), Card(9, 'h'), Card(6, 'd'), None]
        self.players[1].all_hands = [self.players[1].back, self.players[1].mid, self.players[1].front]

        global WIDTH, DEALT_GRAPHICS, BACK_GRAPHICS, MID_GRAPHICS, FRONT_GRAPHICS
        for list_of_graphics in [DEALT_GRAPHICS, BACK_GRAPHICS, MID_GRAPHICS, FRONT_GRAPHICS]:
            if list_of_graphics == DEALT_GRAPHICS:
                for dims in list_of_graphics:
                    self.canvas.create_rectangle(dims, fill = "light green")
            else:
                for dims in list_of_graphics:
                    self.canvas.create_rectangle(dims, fill = "green")

        i = 0
        while i < len(self.players):
            new_small_board = []
            for list_of_graphics in [BACK_GRAPHICS_SMALL, MID_GRAPHICS_SMALL, FRONT_GRAPHICS_SMALL]:
                new_small_row = []
                for dims in list_of_graphics:
                    offset_dims = [dims[0] + GRAPHICS_SMALL_OFFSETS[i][0], dims[1] + GRAPHICS_SMALL_OFFSETS[i][1],
                                   dims[2] + GRAPHICS_SMALL_OFFSETS[i][0], dims[3] + GRAPHICS_SMALL_OFFSETS[i][1]]
                    new_small_row.append(offset_dims)
                    self.canvas.create_rectangle(offset_dims, fill = "green")
                new_small_board.append(new_small_row)
            self.small_boards.append(new_small_board)

            i += 1

        self.turn(self.current_player, 1)




# Create and play a new game when the program is run
game = Game()
game.play_game()
game.root.mainloop()

"""
TO DO:
- Pinapple
- FantasyLand
- Make it so cards follow mouse while they are being moved
- Server-client interactions
- AI?
"""