import requests
import collections
import csv

SP_file = 'FantasyPros_2020_Projections_SP.csv'
RP_file = 'FantasyPros_2020_Projections_RP.csv'
H_file = 'FantasyPros_2020_Projections_H.csv'


class Player:
    """
    Player class models an individual player
    """
    def __init__(self, name, team, positions, proj_points):
        self.name = name
        self.team = team
        self.positions = positions
        self.proj_points = proj_points

    def __eq__(self, other):
        return self.proj_points == other.proj_points and self.name == other.name

    def __lt__(self, other):
        if self.proj_points != other.proj_points:
            return self.proj_points < other.proj_points
        return self.name < other.name



class PlayerDatabase:
    """
    This class is used to parse the csv files and convert them into a player database.
    It will then convert the player's projections into points projections based on the point system brought in.
    """

    def __init__(self, point_system):
        self.point_system = point_system

    IBB_HBP_ASSUMPTION = .05

    def __loadHitterData(self):
        """
        Loads the hitter file into a vector of hitters
        """
        hitter_data = []
        with open(H_file, newline='') as f:
            data = csv.reader(f)
            first = True
            relevant_indices = {}
            ab_index = -1
            for row in data:
                if len(row) <= 1:
                    continue
                if first:
                    for i in range(len(row)):
                        if row[i] in self.point_system[0]:
                            relevant_indices[row[i]] = i
                        elif row[i] == 'H':
                            relevant_indices['H'] = i
                        elif row[i] == 'AB':
                            ab_index = i
                    first = False
                else:
                    proj_points = 0
                    non_singles = 0
                    for category in relevant_indices:
                        if category != 'H':
                            proj_points += int(row[relevant_indices[category]]) * self.point_system[0][category]
                            if category == '2B' or category == '3B' or category =='HR':
                                non_singles += int(row[relevant_indices[category]])
                    proj_points += (int(row[relevant_indices['H']]) - non_singles) * self.point_system[0]['1B']
                    proj_points += round(int(row[ab_index]) * self.IBB_HBP_ASSUMPTION * self.point_system[0]['BB'])
                    hitter_data.append(Player(row[0], row[1], row[2].split(','), round(proj_points)))
        hitter_data.sort(reverse=True)
        return hitter_data

    def __loadParticularPitcherData(self, file, individual_categories):
        """
        Loads one of the two provided pitcher files
        """
        with open(file, newline='') as f:
            data = csv.reader(f)
            first = True
            relevant_indices = {}
            for row in data:
                if len(row) <= 1:
                    continue
                if first:
                    for i in range(len(row)):
                        if row[i] in self.point_system[1]:
                            relevant_indices[row[i]] = i
                    first = False
                else:
                    pitcher_info = row[0] + "_" + row[1] + "_" + row[2]
                    individual_categories[pitcher_info] = {}
                    for category in relevant_indices:
                        individual_categories[pitcher_info][category] = float(row[relevant_indices[category]])


    def __loadPitcherData(self):
        """
        This function loads all of the pitcher data in a list of pitchers and returns it to the callee
        """
        pitcher_data = []
        individual_categories = {}
        self.__loadParticularPitcherData(SP_file, individual_categories)
        self.__loadParticularPitcherData(RP_file, individual_categories)
        for player in individual_categories:
            proj_points = 0
            for category in individual_categories[player]:
                proj_points += individual_categories[player][category] * self.point_system[1][category]
            pitcher_info = player.split('_')
            pitcher_data.append(Player(pitcher_info[0], pitcher_info[1], pitcher_info[2].split(','), round(proj_points)))
        pitcher_data.sort(reverse=True)
        return pitcher_data

    # def __isSamePerson(self, hitter, pitcher):
    #
    #     if hitter.name != pitcher.name:
    #         return False
    #     if hitter.team != pitcher.name:
    #         return False
    #     return hitter.positions == pitcher.positions

    def __mergeArrays(self, hitter_data, pitcher_data, projections):
        """
        This function merges the arrays such that they remain in order from highest to lowest
        """
        uniquePlayers = {}
        duplicates = set()
        for i in range(len(hitter_data)):
            uniquePlayers[(hitter_data[i].name, hitter_data[i].team)] = i
        for j in range(len(pitcher_data)):
            # Have to do this check because of Shohei Ohtani (A starting pitcher and a designated hitter), what a pain...
            if (pitcher_data[j].name, pitcher_data[j].team) in uniquePlayers:
                hitter_data[uniquePlayers[(pitcher_data[j].name, pitcher_data[j].team)]].proj_points += pitcher_data[j].proj_points
                duplicates.add(j)
            uniquePlayers[(pitcher_data[j].name, pitcher_data[j].team)] = j
        for index in duplicates:
            pitcher_data.remove(pitcher_data[index])
        hitter_data.sort(reverse=True)
        hitter_index = 0
        pitcher_index = 0
        while hitter_index < len(hitter_data) and pitcher_index < len(pitcher_data):
            projections.append(hitter_data[hitter_index] if hitter_data[hitter_index] > pitcher_data[pitcher_index] else pitcher_data[pitcher_index])
            if hitter_data[hitter_index] > pitcher_data[pitcher_index]:
                hitter_index += 1
            else:
                pitcher_index += 1
        while hitter_index < len(hitter_data):
            projections.append(hitter_data[hitter_index])
            hitter_index += 1
        while pitcher_index < len(pitcher_data):
            projections.append(pitcher_data[pitcher_index])
            pitcher_index += 1

    def getPlayerIndex(self):
        """
        Returns array of player names to indices
        """
        playerIndex = {}
        for i in range(len(self.projections)):
            playerIndex[self.projections[i].name] = i
        return playerIndex

    def loadProjectionData(self):
        """
        Returns an ordered list of mlb players based on how many projected points they are expected to have
        """
        projections = []
        hitter_data = self.__loadHitterData()
        pitcher_data = self.__loadPitcherData()
        self.__mergeArrays(hitter_data, pitcher_data, projections)
        self.projections = projections
        return projections
