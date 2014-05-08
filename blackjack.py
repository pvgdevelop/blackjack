# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (90, 127.75)
CARD_CENTER = (45, 63.9)
card_images = simplegui.load_image("https://dl.dropbox.com/s/lw0mgt9smno7sa0/card_deck.png")

CARD_BACK_SIZE = (90, 127.75)
CARD_BACK_CENTER = (45, 63.9)
card_back = simplegui.load_image("https://dl.dropbox.com/s/ix4j953crd9p6cq/card_back.png")

# initialize some useful global variables
pos_dealer = [100, 200]
pos_player = [100, 400]
in_play = False
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        msg = "Hand contains"
        for card in self.cards:
            msg += ' ' + str(card)
        return msg

    def add_card(self, card):
        return self.cards.append(card)

    def get_value(self):
        has_no_ace = True
        hand_value = 0

        for card in self.cards:
            if card.get_rank() == 'A':
                has_no_ace = False
            hand_value += VALUES[card.get_rank()]

        if has_no_ace:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value

    def draw(self, canvas, pos):
        self.pos = pos
        for c, i in zip(self.cards,
                        range(len(self.cards))):
            if i > 0:
                self.pos[0] += 10 + CARD_SIZE[0]
            c.draw(canvas, self.pos)


class Deck:
    def __init__(self):
        self.deck = []

        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)

    def shuffle(self):
        return random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(0)

    def __str__(self):
        msg = "Deck contains"
        for card in self.deck:
            msg += ' ' + str(card)
        return msg


def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, score
    if in_play:
        score -= 1
    outcome = "Hit or Stand?"

    # your code goes here
    deck = Deck()
    deck.shuffle()

    # Deal player and dealer cards
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    in_play = True


def hit():
    global outcome, in_play, score

    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted!"
            in_play = False
            score -= 1
    return


def stand():
    global outcome, in_play, score

    if not in_play:
        return
    else:
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())

            if dealer_hand.get_value() > 21:
                outcome = "You win"
                score += 1
                return

    if dealer_hand.get_value() >= player_hand.get_value():
        outcome = "You lose"
        score -= 1
        return
    else:
        outcome = "You win"
        score += 1
        return


def draw(canvas):

#   Call draw method of Hand class on player and dealer hand
    player_hand.draw(canvas, [60,400])
    dealer_hand.draw(canvas, [60,200])

#   Draw flipped card when players turn.
    if in_play:
#       Draw green box to covers dealers card while card_back image is loading
        canvas.draw_line((205,200), (205, CARD_BACK_SIZE[1] + 205), 95, 'Green')
#       Draw card_back image
        card_loc = (CARD_BACK_CENTER[0],
                    CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [70 + CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    else:
#       Dealers Score
        canvas.draw_text("Dealer: " + str(dealer_hand.get_value()), [100, 180], 30, "Black")

    canvas.draw_text("Blackjack", [200, 50], 50, "Black")
    canvas.draw_text(outcome, [150, 380], 40, "White")
    canvas.draw_text("Score: " + str(score), [330, 140], 50, "White")

    canvas.draw_text("You have: " + str(player_hand.get_value()), [100, 570], 30, "Black")

    if outcome != "Hit or Stand?":
        canvas.draw_text("Deal?", [100, 140], 50, "White")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric