#!/usr/bin/env python3

import pdb
from PlayerDatabaseClass import PlayerDatabase
from MyTeamClass import MyTeam

batter_categories = ['R', '1B', '2B', '3B', 'HR', 'RBI', 'BB', 'K', 'SB']
pitcher_categories = ['IP', 'H', 'ER', 'BB', 'K', 'QS', 'CG', 'W', 'L', 'SV', 'BS', 'HD']
dBatter_scoring = {'R': 2, '1B': 2, '2B': 4, '3B': 6, 'HR': 8, 'RBI': 2, 'BB': 2, 'K': -1, 'SB': 2}
dPitcher_scoring = {'IP': 6, 'H': -2, 'ER': -4, 'BB': -2, 'K': 2, 'QS': 3, 'CG': 5, 'W': 7, 'L': -6, 'SV': 7, 'BS': -6, 'HD': 2}
roster_poitions = ['C', '1B', '2B', '3B', 'SS', '2B/SS', '1B/3B', 'IF', 'LF', 'CF', 'RF', 'OF', 'DH', 'UTIL', 'P', 'SP', 'RP']
# dMinPerPosition = {'C': 1, '1B': 1, '2B': 1, '3B': 1, 'SS': 1, 'OF': 5, '2B/SS': 1, '1B/3B': 1, 'UTIL': 1, 'P': 9}
# dMaxPerPosition = {}
dMinPerPosition = {'C': 1, '1B': 1, '2B': 1, '3B': 1, 'SS': 1, 'OF': 4, '2B/SS': 1, '1B/3B': 1, 'UTIL': 3, 'SP': 5, 'RP': 1}
dMaxPerPosition = {'C': 3, 'SP': 7, 'RP': 3}
dTeamSize = 26

def getYesOrNo(prompt):
    """
    This function merely extracts a yes or no response from the user.
    """
    while True:
        string = input(prompt)
        if len(string) == 0:
            continue
        if string[0] == 'Y' or string[0] == 'y':
            return True
        if string[0] == 'N' or string[0] == 'n':
            return False
        print('Please enter Yes or No')


def getPointSystem():
    """
    This function is used to learn what scoriung system it should enforce in its projections
    """
    print('There is a standard scoring system from ESPN which is this program\'s default scoring system.')
    if getYesOrNo('Would you like to use this program\'s default scoring? '):
        return (dBatter_scoring, dPitcher_scoring)
    else:
        print('Please enter the associated points with each category.')
        print('Batter stats:')
        hitter_point_system = []
        for i in batter_categories:
            while True:
                try:
                    hitter_point_system.append(float(input(i + ': ')))
                    break
                except ValueError:
                    print('Please enter a numeric value')
        print('Pitcher stats:')
        pitcher_point_system = []
        for j in pitcher_categories:
            while True:
                try:
                    pitcher_point_system.append(float(input(j + ': ')))
                    break
                except ValueError:
                    print('Please enter a numeric value')
        return (dict(zip(batter_categories, hitter_point_system)), dict(zip(pitcher_categories, pitcher_point_system)))

def getResponse(message, min, max):
    """
    This function extracts a numerical response from the user with the given constraints
    """
    temp = 0
    while True:
        try:
            temp = int(input(message))
            if temp < min or temp > max:
                raise ValueError
            return temp
        except ValueError:
            print('Please enter an integer value between ' + str(min) + ' and ' + str(max) + '.')

def fillRequirements(team_size, min):
    """
    This function will iterate through the positions in order to get the custom roster restrictions for your league
    """
    print('If you don\'t want to enforce a restriction for a certain position, enter \'-1\'.')
    map = {}
    restrictions = 0
    insert = 'minimum (i.e. how many starters for that position)' if min else 'maximum'
    for pos in roster_poitions:
        while True:
            try:
                num = int(input('What is the ' + insert + ' number of players for ' + pos + '? '))
                if num < 0:
                    if num == -1:
                        break
                    raise ValueError
                restrictions += num
                if min and restrictions > team_size:
                    print('The number of minimum requirements is greater than the total number of roster slots.  Please re-enter you restrictions')
                    return fillRequirements(team_size, min)
                break
            except ValueError:
                print('Please enter an integer')



def getLeagueInfo(minPerPosition, maxPerPosition):
    """
    This function fills out a lot of the basic information about your league before you start your draft
    """
    team_size = 0
    print('There are many different lineup and roster constructions in fantasy leagues.')
    print('This program offers ESPN\'s default lineup as the default for this program.')
    if getYesOrNo('Would you like to use the default lineup construction via ESPN? '):
        print('Here is the default roster that you want to try to fill.')
        for pos in dMinPerPosition:
            for i in range(dMinPerPosition[pos]):
                print(pos + ': ')
            minPerPosition[pos] = dMinPerPosition[pos]
        for pos in dMaxPerPosition:
            maxPerPosition[pos] = dMaxPerPosition[pos]
        team_size = dTeamSize
        print()
    else:
        team_size = getResponse('How many players are on a team roster (excluding IL spots)? ', minRosterSize, maxRosterSize)
        minPerPosition = fillRequirements(team_size, False)
        maxPerPosition = fillRequirements(team_size, True)
    return team_size

def getPickResult(draft_pick, availablePlayers, playerIndex):
    """
    This function gets the result of a particular pick and will check to see that it isnt already taken or doesnt exist
    """
    while True:
        player = input('Who was selected with pick ' + str(draft_pick + 1) + '? ')
        if player not in playerIndex:
            print('That player does not exist in our database.  Please re-enter the draft selection.')
            continue
        if playerIndex[player] not in availablePlayers:
            print(player + ' was already selected.  Please re-enter the draft selection.')
            continue
        return playerIndex[player]

def isOurPick(draft_pick, teams, draft_pos):
    """
    Checks to see if this pick is our draft pick
    """
    if (draft_pick % teams) == draft_pos - 1 and (draft_pick // teams) % 2 == 0: # For odd number rounds (draft_pick // teams is 0 indexed)
        return True
    if (draft_pick % teams) == teams - draft_pos and (draft_pick // teams) % 2 == 1: # For even number rounds
        return True
    return False

def computeAddedValue(possibility, projections):
    """
    Iterates through the players to compute the projected added value
    """
    points = 0
    for player in possibility:
        points += projections[player].proj_points
    return points

def generateAllPossibilities(availablePlayers, projections, myteam, round, group1, group2, isGroup1, possibility, possibilities, maxNumLevels):
    """
    This function iterates through all of the possibilities of teams stemming from a certain pick (i.e. the first player in possibility).
    It populates possibilities with each combination it finds.  It has to alternate how many players it considers each time due to the snake draft
    style.  Therefore, it has to alternate between group1 and group2 (both calculate number of picks in between your current pick and your next pick)
    """
    if round > myteam.team_size or len(possibility) >= maxNumLevels:
        possibilities.append(possibility)
        return
    considerations = []
    non_considerations = []
    counter = 0
    while counter < (group1 if isGroup1 else group2):
        player = availablePlayers.pop()
        players = [projections[i] for i in possibility]
        players.append(projections[player])
        if myteam.fulfillsMaxRequirements(players) and myteam.fulfillsMinRequirements(players):
            considerations.append(player)
            counter += 1
        else:
            non_considerations.append(player)
    for i in range(len(considerations)):
        copy = possibility.copy()
        copy.append(considerations[i])
        generateAllPossibilities(availablePlayers, projections, myteam, round + 1, group1, group2, not isGroup1, copy, possibilities, maxNumLevels)

    c_index = len(considerations) - 1
    nc_index = len(non_considerations) - 1
    while c_index >= 0 and nc_index >= 0:
        if considerations[c_index] > non_considerations[nc_index]:
            availablePlayers.append(considerations[c_index])
            c_index -= 1
        else:
            availablePlayers.append(non_considerations[nc_index])
            nc_index -= 1
    while c_index >= 0:
        availablePlayers.append(considerations[c_index])
        c_index -= 1
    while nc_index >= 0:
        availablePlayers.append(non_considerations[nc_index])
        nc_index -= 1

def computeOptimalPicks(availablePlayers, projections, playerIndex, myteam, teams, draft_pick, maxNumLevels):
    """
    This pick computes the average added value to your team for each of the next best player available.  It will then return the ordered list of players to the caller.
    """
    group1 = (teams - draft_pick % teams) + (teams - (draft_pick + 1) % teams)
    group2 = 2 * teams - group1
    considerations = {}
    best_picks = {}
    to_reappend = []
    counter = 0
    while counter < group1:
        player = availablePlayers.pop()
        to_reappend.append(player)
        if myteam.fulfillsMaxRequirements([projections[player]]) and myteam.fulfillsMinRequirements([projections[player]]):
            considerations[player] = []
            counter += 1
    for player in considerations:
        possibility = [player]
        generateAllPossibilities(availablePlayers, projections, myteam, ((draft_pick + 1) // teams) + 1, group1, group2, False, possibility, considerations[player], maxNumLevels)
        added_value = 0
        for j in range(len(considerations[player])):
            added_value += computeAddedValue(considerations[player][j], projections)
        best_picks[player] = added_value / len(considerations[player])
    to_reappend.sort(reverse=True)
    for i in range(len(to_reappend)):
        availablePlayers.append(to_reappend[i])
    return best_picks

def simulateDraft(projections, playerIndex, teams, draft_pos, myteam, maxNumLevels):
    """
    This function handles the draft simulation and calls many helper functions which handle the more specific details of the draft.
    """
    availablePlayers = []
    for player in projections[::-1]:
        availablePlayers.append(playerIndex[player.name])
    for draft_pick in range(myteam.team_size * teams):
        print()
        top_10 = availablePlayers[len(availablePlayers) - 1:len(availablePlayers) - 11: -1]
        print('Here are the top 10 players on the board')
        for p_index in top_10:
            print(projections[p_index].name + str(projections[p_index].positions) + ': ' + str(projections[p_index].proj_points))
        if isOurPick(draft_pick, teams, draft_pos):
            print('\nMy Pick!  Here is the average value added to your team over the next ' + str(maxNumLevels) + ' rounds for next best available players.')
            optimal_picks = computeOptimalPicks(availablePlayers, projections, playerIndex, myteam, teams, draft_pick, maxNumLevels)
            for player in optimal_picks:
                print(projections[player].name + ' ' + str(projections[player].positions) + ': ' + str(optimal_picks[player]))
            print()
            while True:
                pick = getPickResult(draft_pick, availablePlayers, playerIndex)
                if myteam.fulfillsMaxRequirements([projections[pick]]) and myteam.fulfillsMinRequirements([projections[pick]]):
                    break
                else:
                    print('You are unable to pick this player due to the roster construction restrictions.  Please re-enter the draft selection.')
            myteam.add(projections[pick])
            availablePlayers.remove(pick)
        else:
            pick = getPickResult(draft_pick, availablePlayers, playerIndex)
            availablePlayers.remove(pick)

def intro():
    print('\nWelcome to My Assistant GM!')
    print('The aim of this program is to assist in maximizing your return on fantasy baseball drafting by optimizing for positional scarcity.')
    print('This program is meant to be run interactively alongside a fantasy baseball snake draft, and you should update this program as players come off the board.')
    print('Once your turn arrives, it will project over the a certain amount of future rounds to see which players remaining will yield the highest average added value')
    print('Note: at the beginning of draft the impact of this program will be minimal due to the large array of options available.')
    print('In other words, if the number of rounds you wish to project out is greater than the number of players remaining on your roster for any position.')
    print('For example, if it projects out 7 rounds and you have 4 of your maximum 7 pitchers, it will provide more telling information Due to roster restrictions.')
    print('The projections were taken from fantasypros.com and the roster construction is recreated from ESPN\'s fantasy baseball platform.')
    print('This program is not intended for outside distribution and all rights remain with the MLB, ESPN, and fantasypros.')
    print('Once you are ready to enter into the simulator, press [enter]')
    print('If you want to learn more about the assumptions that this program made, enter \'More\'')
    str = input()
    if str == 'More':
        print('Fantasy baseball (as well as other sports) can be very unpredictable and dependent on who you are drafting with.')
        print('This program tries its best to simulate the average conditions in an average draft.')
        print('The following are some of the assumptions/restrictions that this program follows:')
        print('1. For each of your picks, it assumes that the number of players that you should \'consider\' is the number of draft slots')
        print('\tin between the current pick and your next pick. This is because it assumes that the other players will pick the next best player.')
        print('2. It follows the projections (credits to fantasypros) and believes that each player will reach that projection. Obviously drafters')
        print('\ttake into account players who are \'sleeper\' or \'busts\'. But this program is not meant to do that.')
        print('3. It only projects out a fixed number rounds into the future so as to minimize computation time.')
        print('4. It assumes that a HBP or an IBB happens a fixed amount of times during a season (based on how many plate ')
        print('\t appearances the batter is projcted) as well as HBP and IBB being weighted equal to a walk.\n')



minNumTeams = 2
maxNumTeams = 20
minRosterSize = 7
maxRosterSize = 30
kMinRounds = 5
kMaxRounds = 30
def main():
    intro()
    point_system = getPointSystem()
    pd = PlayerDatabase(point_system)
    projections = pd.loadProjectionData()
    playerIndex = pd.getPlayerIndex()
    teams = getResponse('How many teams are in your league (including yourself)? ', minNumTeams, maxNumTeams)
    draft_pos = getResponse('What is your draft position in your snake draft? ', 1, teams)
    minPerPosition, maxPerPosition = {}, {}
    team_size = getLeagueInfo(minPerPosition, maxPerPosition)
    print('Starting the draft simulation...\n')
    myteam = MyTeam(minPerPosition, maxPerPosition, team_size)
    maxNumLevels = getResponse('How many rounds out do you want to project for each pick? ', kMinRounds, kMaxRounds)
    myteam.setNumLevels(maxNumLevels)
    simulateDraft(projections, playerIndex, teams, draft_pos, myteam, maxNumLevels)
    print('Thank you for drafting with us!')


if __name__ == '__main__':
    main()
