#How close would the election result 'flip'? 

#1st Step: creating object class 'State'
class State():
    """
    A class representing the election results for a given state. 
    Assumes no ties between dem and gop votes. The party with a 
    majority of votes receives all the Electoral College (EC) votes for 
    the given state.
    """

    def __init__(self, name, dem, gop, ec):
        """
        Parameters:
        name - the 2 letter abbreviation of a state
        dem - number of Democrat votes cast
        gop - number of Republican votes cast
        ec - number of EC votes a state has 

        Attributes:
        self.name - str, the 2 letter abbreviation of a state
        self.winner - str, the winner of the state, "dem" or "gop"
        self.margin - int, difference in votes cast between the two parties, a positive number
        self.ec - int, number of EC votes a state has
        """
        self.name = name
        self.ec = ec
        self.margin = abs(dem-gop)
        #The winning party has more votes cast
        self.winner = 'dem' if dem > gop else 'gop' 

    def get_name(self):
        """
        Returns:
        str, the 2 letter abbreviation of the state  
        """
        return self.name 

    def get_num_ecvotes(self):
        """
        Returns:
        int, the number of EC votes the state has 
        """
        return self.ec

    def get_margin(self):
        """
        Returns: 
        int, difference in votes cast between the two parties, a positive number
        """
        return self.margin

    def get_winner(self):
        """
        Returns:
        str, the winner of the state, "dem" or "gop"
        """
        return self.winner
    
    #Calling print(object) directs to __str__ method
    def __str__(self):
        """
        Returns:
        str, representation of this state in the following format,
        "In <state>, <ec> EC votes were won by <winner> by a <margin> vote margin."
        """
        #%s, %d act as place-holders for respective str and int type variables
        return 'In %s, %d EC votes were won by %s by a %d vote margin.' % (self.name, self.ec, self.winner, self.margin)

    def __eq__(self, other):
        """
        Determines if two State instances are the same.

        Parameter:
        other - State object to compare against  

        Returns:
        bool, True if the two states are the same, False otherwise
        """
        #__dict__ contains all variable attributes
        #isinstance() makes sure the caller variable is a State object
        #Avoid potential __eq__ functions miscall and mis-return 
        if isinstance(other, State):
            return self.__dict__ == other.__dict__

#2nd Step: Load simplified election data from a file 
def load_election(filename):
    """
    Reads the contents of a file, with data given in the following tab-delimited format,
    State   Democrat_votes    Republican_votes    EC_votes 

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    #Declare storage variables for later return 
    vote_results = open(filename)
    state_results = []
    #Loop through each line of file 
    for line in vote_results: 
        #Every line is a list representing a state
        state = line.split()  
        #Omit the first line representing the header
        if state[0] != 'State':
            state_results.append(State(state[0], int(state[1]), int(state[2]), int(state[3])))
    return state_results

#3rd Step: Find winner in an election based on EC votes
def find_winner(election):
    """
    Note: because election is simplfied, 
    all of EC votes from a state go to the party with the majority vote.

    Parameters:
    election - a list of State instances 

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'gop') if Democrats won, else ('gop', 'dem')
    """
    #Create storage variables for EC votes of both parties
    dem, gop = 0, 0
    #Loop through states to retrieve a total count of wins 
    for state in election:
        if state.get_winner() == 'dem':
            dem+=state.get_num_ecvotes()
        else:
            gop+=state.get_num_ecvotes()
    #Define the tuple ec_result as the order (winner, loser)
    ec_result = ('dem', 'gop') if dem>gop else ('gop', 'dem')
        
    return ec_result
    
def get_winner_states(election):
    """
    Finds the list of States that were won by the winning candidate (lost by the losing candidate).

    Parameters:
    election - a list of State instances 

    Returns:
    A list of State instances won by the winning candidate
    """
    #Create storage variable for states won by both parties
    dem_states, gop_states = [], []
    #Loop through all states 
    for state in election:
        #CASE 1: Democrat states
        if state.get_winner() == 'dem':
            dem_states.append(state)
        #CASE 2: Republican states
        else:
            gop_states.append(state)
    #Checkpoint: both party state lists are filled
    return dem_states if find_winner(election) == ('dem', 'gop') else gop_states
            
def ec_votes_reqd(election, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election - a list of State instances 
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    #Declare storage variable for total winner EC votes
    dem, gop = 0, 0
    #Loop through states to retrieve a total count of wins 
    for state in election:
        if state.get_winner() == 'dem':
            #all the EC votes of Democrats
            dem+=state.get_num_ecvotes()
        else:
            #all the EC votes of Republicans
            gop+=state.get_num_ecvotes()

    #Return least EC votes needed to win minus the current votes for loser 
    #CASE 1 (IF): Democrats lose                #CASE 2 (ELSE): Republicans lose
    return int(abs(total/2 + 1 - dem)) if gop > dem else int(abs(total/2 + 1 - gop))
    
#4th Step: Greedy algorithm 
def greedy_election(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. 
    
    First, choose the states with the smallest 
    win margin, i.e. state that was won by the smallest difference in number of voters. 
    
    Then, choose other states up until it meets or exceeds the ec_votes_needed
    
    Return states that were originally won by the winner in the election.

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    
    Empty list, if no possible swing states
    """
    #Create variable to store culmulative change in EC votes
    ec_change = 0
    #Create list to store subset of states from winner states 
    swing_states = []
    #Sort in ascendng order by margin
    sorted_winner = sorted(winner_states, key=lambda x: (x.get_margin(), -x.get_num_ecvotes()))
    for state in sorted_winner: 
        #Update ec_change with the respective state EC votes
        ec_change+=state.get_num_ecvotes()
        swing_states.append(state) 
        #Return as soon as EC change exceeds votes needed
        #Include the last state at the moment of going over
        if ec_change >= ec_votes_needed:
            return swing_states
        #CASE 2: swing_states is empty 
        if not swing_states:
            return swing_states

#5th Step: Moving voters around
def dp_move_max_voters(winner_states, ec_votes, memo=None):
    """
    Finds the largest number of voters needed to relocate to get at most ec_votes
    for the election loser. 

    Analogy to the knapsack problem:
    Given a list of states each with a weight(#ec_votes) and value(#margin),
    determine the states to include in a collection so the total weight(#ec_votes)
    is less than or equal to the given limit(ec_votes) and the total value(#voters displaced)
    is as large as possible.

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes - int, number of EC votes (relocation should result in gain of AT MOST ec_votes)
    memo - dictionary for memorization 

    Returns:
    A list of State instances such that the maximum number of voters need to be relocated
    to these states in order to get at most ec_votes 
    
    Empty list, if every state has a # EC votes greater than ec_votes
    """
    #establish helper function to be called
    def max_voter(winner_states, ec_votes, memo=None):
        #Set memo to empty dictionary 
        if memo is None: 
            memo = {}
        #CASE 0: In Memo
        #Store memo key as tuple (length, weight)
        if (len(winner_states), ec_votes) in memo.keys():
            return memo[(len(winner_states), ec_votes)]
        #CASE 1: Base Case
        if not winner_states or ec_votes <= 0:
            return (0, [])
        #CASE 2: Recursion
        else:
            #Left branch: check to see if it is possible to take 
            if winner_states[0].get_num_ecvotes() <= ec_votes:
                nextItem = winner_states[0]
                #Explore left branch
                withVal, withToTake = max_voter(winner_states[1:], ec_votes - nextItem.get_num_ecvotes(), memo)
                withVal += nextItem.get_margin()
                #Explore right branch
                withoutVal, withoutToTake = max_voter(winner_states[1:], ec_votes, memo)
                #Choose better branch
                if withVal < withoutVal:
                    #better not take it 
                    result = (withoutVal, withoutToTake)
                    #update memo with the action
                    memo[(len(winner_states), ec_votes)] = result 
                else:
                    #better take it
                    result = (withVal, withToTake+ [nextItem])
                    #update memo with the action
                    memo[(len(winner_states), ec_votes)] = result 
            #Right branch: Too heavy, can't take, skip to next
            else: 
                #slice to go onto next item
                result = max_voter(winner_states[1:], ec_votes, memo)
                memo[(len(winner_states), ec_votes)] = result 
        return result
    
    #return the max voters, whcih is the second element of the tuple 
    return max_voter(winner_states, ec_votes)[1]
    
def move_min_voters(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated. 
    Only return states that were originally won by the winner (lost by the loser)
    of the election.

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    
    Empty list, if no possible swing states
    """
    #declare variable for storage
    min_states = []
    sum_ec = 0
    #loop through winner states
    for state in winner_states:
        #sum up all ec_votes (weights) of these states
        sum_ec+=state.get_num_ecvotes()
    #max_list uses the complement of sum_ec 
    max_list = dp_move_max_voters(winner_states, sum_ec - ec_votes_needed, memo=None)
    
    #loop through winner states
    for state in winner_states: 
        if state not in max_list:
            min_states.append(state)
    return min_states

#Last step: turning the tides
def flip_election(election, swing_states):
    """
    Finds a way to shuffle voters in order to flip an election outcome. 
    Moves voters from states that were won by the losing candidate (states not in winner_states), 
    to each of the states in swing_states.
    
    To win a swing state, (margin + 1) new voters must be moved into that state. 
    
    Any state that voters are moved from should still be won by the loser even after voters are moved.
    California, Washington, Texas, or Tennessee are PROUD STATES: voters don't move from there

    Also finds the number of EC votes gained by this rearrangement, as well as the minimum number of 
    voters that need to be moved.

    Parameters:
    election - a list of State instances representing the election 
    swing_states - a list of State instances where people need to move to flip the election outcome 
                   (result of move_min_voters or greedy_election)

    Return:
    A tuple that has 3 elements in the following order:
        - a dictionary with the following (key, value) mapping: 
            - Key: a 2 element tuple, (from_state, to_state), the 2 letter abbreviation of the State 
            - Value: int, number of people that are being moved 
        - an int, the total number of EC votes gained by moving the voters 
        - an int, the total number of voters moved 
        
    None, if it is not possible to sway the election
    """
    #find margin + 1 of each swing states 
    #ec votes that each of the winning states 
    #ec_vote_required() for the loser 
    #1-less than the margin for states that belonged to the losing party
    #check if these states are in:
    #move on next step
    
    #these states are not considered
    proud_states = ['CA', 'WA', 'TX', 'TN']
    
    #declare storage variables to keep count
    ec_change = 0
    loser = {}
    mapping = {}
    
    #loser states are just not in the winner states but in election
    #margin-1 = jsut the vote to barely win for loser states 
    for state in election:
        #loser states 
        if state not in get_winner_states(election) and state.get_name() not in proud_states:
            #set keys as immutable stirngs as dict cannot contain mutable keys
            loser.update({state.get_name():state.get_margin()-1})
    #loser states with available voters 
    #loop and pack
    for swing in swing_states:
        #voters for losers needed to be added to win
        voters_needed = swing.get_margin() + 1
        #loop through each loser state
        for loser_state in loser.keys():
            #CASE 1: no margin (when loser states ran out of available voters)
            if loser[loser_state] == 0:
                pass
            #CASE 2: no more voters needed, break out of inner for loop
            if voters_needed == 0:
                break 
            #CASE 3: if there are more availabel voters than needed
            if voters_needed <= loser[loser_state]:
                #update mapping
                mapping.update({(loser_state, swing.get_name()): voters_needed})
                #those voters from lost state either donated all or donated or some
                #update 
                loser[loser_state]-=voters_needed
                voters_needed = 0
            #CASE 4: not enough to fill needed to flip
            else: 
                voters_needed-=loser[loser_state]
                mapping.update({(loser_state, swing.get_name()): loser[loser_state]})
                #those voters are no longer avaialble 
                loser[loser_state] = 0            
        ec_change+=swing.get_num_ecvotes()
        #CASE 5: Bernie Sander: Impossible to flip
        if voters_needed > 0: 
            return None 
    #return ()
    return (mapping, ec_change, sum(mapping.values()))
        
if __name__ == "__main__":
    #tests 1st Step
    ma = State("MA", 100000, 20000, 8)
    print(isinstance(ma, State))
    print(ma)

    #test 2nd Step 
    year = 2012
    election = load_election("%s_results.txt" % year)
    print(len(election))
    print(election[0])

    #test 3rd Step
    winner, loser = find_winner(election)
    won_states = get_winner_states(election)
    names_won_states = [state.get_name() for state in won_states]
    ec_votes_needed = ec_votes_reqd(election)
    print("Winner:", winner, "\nLoser:", loser)
    print("States won by the winner: ", names_won_states)
    print("EC votes needed:",ec_votes_needed, "\n")

    #test 4th Step
    print("greedy_election")
    greedy_swing = greedy_election(won_states, ec_votes_needed)
    names_greedy_swing = [state.get_name() for state in greedy_swing]
    voters_greedy = sum([state.get_margin()+1 for state in greedy_swing])
    ecvotes_greedy = sum([state.get_num_ecvotes() for state in greedy_swing])
    print("Greedy swing states results:", names_greedy_swing)
    print("Greedy voters displaced:", voters_greedy, "for a total of", ecvotes_greedy, "Electoral College votes.\n")

    #test 5th Step - MAX
    print("dp_move_max_voters")
    total_lost = sum(state.get_num_ecvotes() for state in won_states)
    move_max = dp_move_max_voters(won_states, total_lost-ec_votes_needed)
    max_states_names = [state.get_name() for state in move_max]
    max_voters_displaced = sum([state.get_margin()+1 for state in move_max])
    max_ec_votes = sum([state.get_num_ecvotes() for state in move_max])
    print("States with the largest margins:", max_states_names)
    print("Max voters displaced:", max_voters_displaced, "for a total of", max_ec_votes, "Electoral College votes.", "\n")

    #test 5th Step  - MIN
    print("move_min_voters")
    swing_states = move_min_voters(won_states, ec_votes_needed)
    swing_state_names = [state.get_name() for state in swing_states]
    min_voters = sum([state.get_margin()+1 for state in swing_states])
    swing_ec_votes = sum([state.get_num_ecvotes() for state in swing_states])
    print("Complementary knapsack swing states results:", swing_state_names)
    print("Min voters displaced:", min_voters, "for a total of", swing_ec_votes, "Electoral College votes. \n")

    #test Last Step
    print("flip_election")
    flipped_election = flip_election(election, swing_states)
    print("Flip election mapping:", flipped_election)