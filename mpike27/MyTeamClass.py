from PlayerDatabaseClass import Player

# i.e. A Catcher also identifies as an infielder as well as a general Utility Player.
broaderPositions = {'C': ['IF', 'UTIL'], '1B': ['1B/3B', 'IF', 'UTIL'], '2B': ['2B/SS', 'IF', 'UTIL'], '3B': ['1B/3B', 'IF', 'UTIL'], 'SS': ['2B/SS', 'IF', 'UTIL'], '2B/SS': ['IF', 'UTIL'], '1B/3B': ['IF', 'UTIL'], 'IF': ['UTIL'], 'LF': ['OF', 'UTIL'], 'CF': ['OF', 'UTIL'], 'RF': ['OF', 'UTIL'], 'OF': ['UTIL'], 'DH': ['UTIL'], 'UTIL': [], 'P': [], 'SP': ['P'], 'RP': ['P']}
upperBound = 10

class MyTeam:
    """
    This class represents one person's team (in this class your team)
    """
    def __init__(self, mins, maxes, team_size):
      self.mins = mins
      self.maxes = maxes
      self.team_size = team_size
      self.currentTeam = [] # Your current players
      self.current_positions = {}
      for pos in broaderPositions:
          self.current_positions[pos] = 0

    def add(self, player):
        """
        Adds a player to your team
        """
        self.currentTeam.append(player)
        positions_to_update = set()
        for pos in player.positions:
            positions_to_update.add(pos)
            for b_pos in broaderPositions[pos]:
                positions_to_update.add(b_pos)
        for update_pos in positions_to_update:
            self.current_positions[update_pos] += 1

    def setNumLevels(self, numLevels):
        self.numLevels = numLevels

    def __recfulfillsMinRequirements(self, players, unfulfilled):
        """
        This helper function recursively solves the minimization problem by exploring all possible combinations of positions
        and if there is a combination that fulfills the minimum requirement it returns true
        """
        if len(players) == 0:
            return len(unfulfilled) == 0
        p_copy = players.copy()
        u_copy = unfulfilled.copy()
        player = players[0]
        del p_copy[0]
        for pos in player.positions:
            if pos in unfulfilled:
                if unfulfilled[pos] == 1:
                    del u_copy[pos]
                    if self.__recfulfillsMinRequirements(p_copy, u_copy):
                        return True
                    u_copy[pos] = 1
                else:
                    u_copy[pos] -= 1
                    if self.__recfulfillsMinRequirements(p_copy, u_copy):
                        return True
                    u_copy[pos] += 1
            for b_pos in broaderPositions:
                if b_pos in unfulfilled:
                    if unfulfilled[b_pos] == 1:
                        del u_copy[b_pos]
                        if self.__recfulfillsMinRequirements(p_copy, u_copy):
                            return True
                        u_copy[b_pos] = 1
                    else:
                        u_copy[b_pos] -= 1
                        if self.__recfulfillsMinRequirements(p_copy, u_copy):
                            return True
                        u_copy[b_pos] += 1
        return False



    def fulfillsMinRequirements(self, players):
        """
        Checks that the players that you are considering will still allow you to fulfill the minimum allotment of players
        """
        picks_left = self.team_size - len(self.currentTeam)
        if picks_left >= self.numLevels or picks_left >= upperBound :
            return True
        unfulfilled = {}
        numUnfulfilled = 0
        for min in self.mins:
            if self.current_positions[min] < self.mins[min]:
                temp = self.mins[min] - self.current_positions[min]
                numUnfulfilled += temp
                unfulfilled[min] = temp
        if numUnfulfilled > picks_left:
            return False
        return self.__recfulfillsMinRequirements(players, unfulfilled)


    def fulfillsMaxRequirements(self, players):
        """
        Makes sure that the players you are considering doesn't encroach on the self imposed maximum restrictions
        """
        total_added_positions = {} # All positions to update mapped to how much to increase by
        for i in range(len(players)): # For every player in the list of prospective picks
            added_positions = {}
            for pos in players[i].positions: # For every position for that particular player
                added_positions[pos] = 1 # Update this person's own map two indicate they identify by that position
                for b_pos in broaderPositions[pos]: # Iterate through all of the broader positions that this particular 'pos' also identifes by (i.e 'LF' is also an 'OF')
                    added_positions[b_pos] = 1
            for pos in added_positions: # Update total positions such that it each position for that player increases by 1
            # Have to separate the loops because multiple positions can map to the same broader position.
                if pos in total_added_positions:
                    total_added_positions[pos] += added_positions[pos] #Don't want to increase that broader position by more than 1 for an individual player
                else:
                    total_added_positions[pos] = 1
        for pos in total_added_positions:
            if pos in self.maxes and pos in self.current_positions and total_added_positions[pos] + self.current_positions[pos] > self.maxes[pos]:
                return False
            if pos in self.maxes and total_added_positions[pos] > self.maxes[pos]:
                return False
        return True
