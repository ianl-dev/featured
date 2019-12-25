#Which strategy is the best?

'''
Modern_blackjack is a mini-game for Blackjack strategists in Python.

'''

import random
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from helper import BlackJackCard, CardDecks, Busted

'''
Modern Blackjack - a simplfied game

Work flow:
    1. Deal cards to player and dealer in alternate fashion

    2. Check for initial blackjacks from either player. Any blackjack at this point means game over
           Calculuate the net changes for the player 

    3. If no one has it, deal the player until they stand or bust
           Whenever game busts, the game is over, calculate the net gain/loss of the player

    4. If the player 'survives', deal the dealer until they stand or bust.
           Whenever game busts, the game is over, calculate the net gain/loss of the player

    5. If no one bust, end game and calculate best value of both the player and the dealer's hands
'''

class BlackJackHand:
    """
    A class representing a game of Blackjack.   
    """
    
    #represent different states with string
    hit = 'hit'
    stand = 'stand'
    doubledown = 'doubledown'

    def __init__(self, deck, initial_bet=1.0):
        """
        Parameters:
        deck - An instance of CardDeck that represents the starting shuffled blackjack card deck 
        initial_bet - float, represents the initial bet/wager of the hand

        Attributes:
        self.deck - CardDeck, represents the shuffled card deck for this game of BlackJack
        self.current_bet - float, represents the current bet/wager of the hand
        self.player - list, initialized with the first 2 cards dealt to the player
                      and updated as the player is dealt more cards from the deck
        self.dealer - list, initialized with the first 2 cards dealt to the dealer
                      and updated as the dealer is dealt more cards from the deck

        Deal in following alternate order:
            player, dealer, player, dealer
        """
        self.deck = deck 
        self.current_bet = initial_bet 
        #if deck is not empty 
        self.player = [deck.deal_card()]
        self.dealer = [deck.deal_card()]
        #Following the draw order: player -> dealer 
        self.player.append(deck.deal_card())
        self.dealer.append(deck.deal_card())

    def set_bet(self, new_bet):
        """
        Sets the player's current wager in the game.

        Parameters:
        new_bet - the floating point number representing the new wager for the game.

        """
        self.current_bet = new_bet

    def get_bet(self):
        """
        Returns the player's current wager in the game.

        Returns:
        self.current_bet, the floating point number representing the current wager for the game

        """
        return self.current_bet
    
    #used for testing only
    def set_initial_cards(self, player_cards, dealer_cards):
        """
        Sets the initial cards of the game.
        player_cards - list, containing the inital player cards
        dealer_cards - list, containing the inital dealer cards

        """
        self.player = player_cards[:]
        self.dealer = dealer_cards[:]

    @staticmethod
    def best_value(cards):
        """
        Finds the total value of the cards. All cards must contribute to the
        best sum
        
        Ace can be  1 or 11.

        The best sum is the highest point total not exceeding 21 if possible.
        If it is not possible to keep the total value from exceeding 21, then
        the best sum is the lowest total value of the cards.

        Parameters:
        cards - a list of BlackJackCard instances.

        Returns:
        int, best sum of point values of the cards  
        
        Examples:
            if deck is [3, 7, A, A]:
                both aces have value 1; best value is 12
            if deck is [A, A]: 
                first ace is treated as 11, second as 1; best value is 12
        """        
        #storage for total best value
        total = 0
        aces = 0
        #circulate through the cards
        for card in cards:
            if card.get_rank() == 'A' :
                aces+=1 
            #add static value
            total+=card.get_val()
        
        #Check if total is greater than 21, reset ace value if needed to 11-1 = 10
        while aces > 0 and total > 21:
            total-=10
            aces-=1 
        return total 
              
    def get_player_cards(self):
        """
        Returns:
        list, a copy of the player's cards 
        """
        return self.player.copy()

    def get_dealer_cards(self):
        """
        Returns:
        list, a copy of the dealer's cards 
        """
        return self.dealer.copy()

    def get_dealer_upcard(self):
        """
        Returns the dealer's face up card. We define the dealer's face up card
        as the first card in their hand.

        Returns:
        BlackJackCard instance, the dealer's face-up card 
        """
        return self.dealer.copy()[0]

    # Strategy 1
    def mimic_dealer_strategy(self):
        """
        A playing strategy in which the player uses the same metric as the
        dealer to determine their next move.

        The player will:
            - hit if the best value of their cards is less than 17
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision  
        """
        #decision is defined by strings 'hit' -> draw card,  or 'stand' -> skip to next time step
        return 'hit' if self.best_value(self.player) < 17 else 'stand'

    # Strategy 2
    def peek_strategy(self):
        """
        A playing strategy in which the player knows the best value of the
        dealer's cards.

        The player will:
            - hit if the best value of their hand is less than that of the dealer's
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision
        """
        #decision is defined by strings 'hit' -> draw card,  or 'stand' -> skip to next time step
        return 'hit' if self.best_value(self.player) < self.best_value(self.dealer) else 'stand'

    # Strategy 3
    def simple_strategy(self):
        """
        A playing strategy in which the player will
            - stand if one of the following is true:
                - the best value of player's hand is greater than or equal to 17
                - the best value of player's hand is between 12 and 16 (inclusive)
                  AND the dealer's up card is between 2 and 6 (inclusive)  
            - hit otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision 
        """
        #hit conditions (either, 1 and 2a, 2b)
        if self.best_value(self.player) >= 17: #1
            return 'stand'
        elif self.dealer[0].get_val() in range (2, 7) and self.best_value(self.player) in range(12,17):
            return 'stand'
        else:
            return 'hit' 
        
    # Strategy 4
    def doubledown_strategy(self):
        """
        A playing strategy in which the player will
            - doubledown if the following is true:
                - the best value of the player's cards is 11
            - else they will fall back to using simple_strategy

        NOTE: In Modern Blackjack, a simplified version of 21, "doubling down" is enabled on any turn

        The double down action indicates a special, somewhat risky, but possibly rewarding player
        action. It means the player wishes to double the current bet of the hand, hit one more time,
        and then immediately stand, ending their turn with whatever cards result. 

        This strategy simply consists of siginaling to that the calling function with the action
        BlackJackHand.doubledown when the sum of the players cards is 11, which is a very good 
        position in which to try to double one's bet while getting only one more card. Otherwise,
        the strategy falls back to using the simple_strategy to play normally.

        Returns:
        str, BlackJackHand.doubledown if player_best_score == 11,
             otherwise the return value of calling simple_strategy to play in the default way
        """
        #11 is a sweet spot: get A-10 and still not burst
        if self.best_value(self.player) == 11:
            return BlackJackHand.doubledown
        else: 
            return self.simple_strategy()

    def play_player_turn(self, strategy):
        """
        Plays a full round of the player's turn and updates the player's hand
        to include new cards that have been dealt to the player (a hit). The player
        will be dealt a new card until they stand, bust, or doubledown. 

        When doubling down, the player doubles their bet, receive one final hit, and 
        then they stand. The hit when doubling down (like any hit) can cause the player to 
        go bust.

        NOTE: Receiving the doubledown action from a strategy indicates: 
            - the player wishes to double their current bet,
            - the player receives one last hit,
            - the player then immediately stands, ending their turn

        NOTE: 
            - Whenever hitting, we signal to the caller if the best value of the 
              player's hand becomes greater than 21 (because the player has busted).

        Parameter:
        strategy - function, one of the the 4 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy, BlackJackHand.double_down_strategy)

        Returns:          
        Nothing 
        """
        while strategy(self) != 'stand':
            #CASE 1: Double down
            if strategy(self) == BlackJackHand.doubledown:
                self.set_bet(self.get_bet()*2)
                self.player.append(self.deck.deal_card())
                #Check busted first 
                break
            #CASE 2: Normal hit
            if strategy(self) == 'hit':
                self.player.append(self.deck.deal_card())
        #busted
        if self.best_value(self.player) > 21: 
            raise Busted
        #CASE 3: Stand

    def play_dealer_turn(self):
        """
        Plays a full round of the dealer's turn and updates the dealer's hand
        to include new cards that have been dealt to the dealer. 
        
        The dealer will get a new card as long as the best value of their hand is less
        than 17. 
        
        If they go over 21, they bust.

        This function does not return anything. Instead, it:
            - Adds a new card to self.dealer each time the dealer hits.
            - Raises Busted exception if the
              best value of the dealer's hand is greater than 21.
        """
        #As long as hand is less than 17
        while BlackJackHand.best_value(self.dealer) < 17:
            self.dealer.append(self.deck.deal_card())
        if BlackJackHand.best_value(self.dealer) > 21:
            raise Busted
    
    #debugging purpose
    def __str__(self):
        """
        Returns:
        str, representation of the player and dealer and dealer hands.
        """
        result = 'Player: '
        for c in self.player:
            result += str(c) + ','
        result = result[:-1] + '    '
        result += '\n   Dealer '
        for c in self.dealer:
            result += str(c) + ','
        return result[:-1]

def play_hand(deck, strategy, initial_bet=1.0):
    """
    Plays a hand of Blackjack and determines the amount of money the player
    gets back based on the bet/wager of the hand.

    The player will get:

        - 2.5 times the bet of the hand if the player's first two cards equal 21,
          and the dealer's first two cards do not equal 21.

        - 2 times the bet of the hand if the player wins by having a higher best value than 
          the dealer after the dealer's turn concludes

        - 2 times the bet of the hand if the dealer busts

        - the exact bet amount of the hand if the game ends in a tie. 
          If the player and dealer both get blackjack from their first two cards, 
          this is also a tie.

        - 0 if the dealer wins with a higher best value, or the player busts.

    Parameters:
        deck - an instance of CardDeck
        strategy - function, one of the the four playing strategies defined in BlackJackHand
        initial_bet - float, the amount that the player initially bets (default=1.0)

    Returns:
        tuple (float, float): (amount_wagered, amount_won)
               amount_wagered, the current bet of the hand. Should use hand.get_bet().
               amount_won, the amount of money the player gets back. Should be 0 if they busted and lost.
    """
    #First, deal cards to player, then dealer
    game = BlackJackHand(deck)
    #Then, check initial blackjacks
    if game.best_value(game.get_player_cards())==21:
        #CASE 1: both win initially  (1x)
        if game.best_value(game.get_dealer_cards())==21:
            return (game.get_bet(), game.get_bet())
        #CASE 2: only player gets blackjack initially (2.5x)
        return (game.get_bet(), 2.5*game.get_bet())
    #only dealer gets initial blackjack, lost
    elif game.best_value(game.get_dealer_cards())==21:
        return (game.get_bet(), 0)
    
    #Now, player plays with strategy
    try:
        #keep hitting until stand
        game.play_player_turn(strategy)
    except:
        #busted
        return (game.get_bet(), 0)
    #Now, dealer plays
    try:
        game.play_dealer_turn()
    except:
        #player wins 2x
        return (game.get_bet(), 2*game.get_bet())
    
    #lastly, if both are not busted, compare best values
    if game.best_value(game.get_player_cards()) > game.best_value(game.get_dealer_cards()):
        return (game.get_bet(), 2*game.get_bet())
    #tie
    elif game.best_value(game.get_player_cards()) == game.best_value(game.get_dealer_cards()):
        return (game.get_bet(), game.get_bet())
    #lost
    else:
        return (game.get_bet(), 0)

def run_simulation(strategy, initial_bet=2.0, num_decks=8, num_hands=20, num_trials=100, show_plot=False):
    """
    Runs a simulation
    Generates a Gaussian distribution that shows player's rate of return across all trials

    The normal distribution is based on the mean and standard deviation of 
    the player's rates of return across all trials. 

    Parameters:

        strategy - function, one of the the four playing strategies defined in BlackJackHand
        initial_bet - float, the amount that the player initially bets each hand. (default=2)
        num_decks - int, the number of standard card decks in the CardDeck. (default=8)
        num_hands - int, the number of hands the player plays in each trial. (default=20)
        num_trials - int, the total number of trials in the simulation. (default=100)
        show_plot - bool, True if the plot should be displayed, False otherwise. (default=False)

    Returns:

        tuple:
            - list of the player's rate of return for each trial
            - float, the average rate of return across all the trials
            - float, the standard deviation of rates of return across all trials    
    """
    rates = []
    for trial in range(num_trials):
        deck = CardDecks(num_decks, BlackJackCard)
        gain = 0
        bet = 0
        #multiple hands in a trial
        #a hand can use multiple decks
        for hand in range(num_hands):
            #record gain in a subgame, taking the second element (amount_gained)
            result = play_hand(deck, strategy, initial_bet)
            bet+=result[0]
            gain+=result[1]
        trial_rate = 100*(gain-bet)/(bet)
        rates.append(trial_rate)
    
    if show_plot:
        probability = stats.norm.pdf(sorted(rates), np.mean(rates), np.std(rates))
        plt.plot(sorted(rates), probability)
        plt.hist(sorted(rates), density=True)
        plt.title('Player ROI on Playing ' + str(num_hands) + ' Hands ' + '(' + strategy.__name__ + ')' + \
                  '\n' + '(Mean =' + str(np.mean(rates)) + '%,'  + ' SD = ' + str(np.std(rates))+ '%' +')')
        plt.xlabel('% return')
        plt.show()
        
    return (rates, np.mean(rates), np.std(rates))
        
def run_all_simulations(strategies):
    """
    Runs a simulation for each strategy in strategies
    Generates a single graph with normal distribution plot for each strategy. 

    Parameters:
        strategies - list of strategies to simulate
    """
    for strategy in strategies:
        #returns a list of rates for this strategy
       rate = run_simulation(strategy)[0]
       probability = stats.norm.pdf(sorted(rate), np.mean(rate), np.std(rate))
       plt.plot(sorted(rate), probability, label = strategy.__name__)
    plt.title('Player ROI for Different Strategies')
    plt.xlabel('% return')
    plt.legend()
    plt.show() 
    
if __name__ == '__main__':
  
    run_simulation(BlackJackHand.mimic_dealer_strategy, show_plot=True)
    run_simulation(BlackJackHand.peek_strategy, show_plot=True)
    run_simulation(BlackJackHand.simple_strategy, show_plot=True)
    run_simulation(BlackJackHand.doubledown_strategy, show_plot=True)

    run_all_simulations([BlackJackHand.mimic_dealer_strategy,
                         BlackJackHand.peek_strategy,
                         BlackJackHand.simple_strategy,
                         BlackJackHand.doubledown_strategy])

    run_simulation(BlackJackHand.mimic_dealer_strategy,
                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)

    run_simulation(BlackJackHand.peek_strategy,
                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)

    run_simulation(BlackJackHand.simple_strategy,
                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)

    run_simulation(BlackJackHand.doubledown_strategy,
                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)
