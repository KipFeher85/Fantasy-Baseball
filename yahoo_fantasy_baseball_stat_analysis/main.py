# This is a sample Python script.
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
import statsapi

# Obtain Yahoo OAuth2 access token from the file given
oauth = OAuth2(None, None, from_file='OAuth2.json')

# Create a Yahoo Fantasy MLB Game object using the access token
gm = yfa.Game(oauth, 'mlb')

# Get the league id desired
leagueID = gm.league_ids(year=2021)[0]

print(leagueID)

# Create a league object given the first id of the user's league id's for the season
lg = gm.to_league(leagueID)

# Create a team object given the team's key
tm = lg.to_team(team_key=lg.team_key())

# Create dict to hold ballpark factors, lists to hold NL and AL team names
ballParkDict = {}
alTeamList = []
nlTeamList = []

# Open json file containing teams and ballpark factors as a file object
with open('ballParkFactors.json') as f:
    # Create lists for each team and ballpark factors
    teamList = []
    bfList = []
    # Create json object from file
    data = json.load(f)
    # Add each team and ballpark factor to their respective lists
    for i in range(0, len(data)):
        teamList.append(data[i]['Team'])
        bfList.append(data[i]['Basic'])
# Add every team and their respective ballpark factor to the dict
for i in range(0, len(teamList)):
    ballParkDict.update({teamList[i]: bfList[i]})
# Add every AL team to a list
for i in range(0, 14):
    alTeamList.append(teamList[i])
# Add every NL team to a list
for i in range(14, len(teamList)):
    nlTeamList.append(teamList[i])
# Add a column to the dict for both the NL and AL avg ballpark factor
ballParkDict.update({"NL Avg": data[0]['NL Basic']})
ballParkDict.update({"AL Avg": data[0]['AL Basic']})

class League:
    def getPlayer(self, playerName, type):
        pass
        playerId = lg.player_details(playerName)[0]['player_id']
        playerPos = lg.player_details(playerName)[0]['position_type']
        if playerPos == 'B':
            playerDict = League.getBatter(self, type, playerId)
            League.printBatters(self, type, playerDict)
        else:
            playerDict = League.getPitcher(self, type, playerId)
            League.printPitchers(self, type, playerDict)

    def getCurrentRoster(self):
        pass
        """
        Display's a player's entire roster without their stats but player details (Position, Eligible Postions, Status)
        :return:
        """
        hitterList = []
        pitcherList = []
        injuredList = []

        # Iterate through every player on the team within the current week
        for i in tm.roster(lg.current_week()):
            if i["position_type"] == 'P':
                pitcherList.append(i)
            else:
                hitterList.append(i)
            if i["status"] != '':
                injuredList.append(i)

        print("Hitter List: ")
        for i in hitterList:
            print(i)
        print("Pitcher List: ")
        for i in pitcherList:
            print(i)
        print("Injured List: ")
        for i in injuredList:
            print(i)

    def currentRosterStats(self, type):
        pass
        """
        Display roster and their advanced stats over the desired time period 'type'
        :param type: Time period desired for player stats. Possible values are: 'lastweek', 'lastmonth', and 'season'
        :return:
        """
        print("Your batters: ")
        # Get the dict of all batters currently on your team
        currentBatters = League.getBatters(self, type, 3)
        # Print every batter and their advanced stats in currentBatters
        League.printBatters(self, type, currentBatters)

        print("Your pitchers: ")
        # Get the dict of all pitchers currently on your team
        currentPitchers = League.getPitchers(self, type, 3)
        # Print every pitcher and their advanced stats in currentPitchers
        League.printPitchers(self, type, currentPitchers)

    def teamDetails(self):
        pass
        """
        Gives basic details for every team in the league including name, owner, owner legacy, logo info
        :return:
        """
        # Get dict of all teams in the league
        tms = lg.teams()
        for i in tms:
            print(list(tms[i].items()))

    def predictTeamDay(self):
        pass
        """
        Function to help aid in the selection of players for the daily lineup
        Displays the probable pitchers for every game
        Probable pitcher's name, pregame note, and advanced stats from their past month are shown
        User's batter advanced stats over the past week are displayed as well
        :return:
        """
        # Create a dictionary of all the games being played today
        today = statsapi.schedule()

        # Create lists for both the away and home teams
        hTList = []
        aTList = []

        # Create lists to hold pregame notes for both the home and away pitchers
        hNList = []
        aNList = []

        # Create lists to hold both the home pitcher id and away pitcher
        homePIDList = []
        awayPIDList = []

        # Create lists to hold both the home pitcher and away stat lines
        homePitcherStatList = []
        awayPitcherStatList = []

        # For every game on the schedule
        for game in today:
            hTList.append(game["home_name"])
            aTList.append(game["away_name"])

            hNList.append(game["home_pitcher_note"])
            aNList.append(game["away_pitcher_note"])

            homePitcher = game["home_probable_pitcher"]
            # Get the player_id of the home pitcher
            hPID = lg.player_details(homePitcher)[0]['player_id']
            # Add the homePitcher's name and id to the list
            homePIDList.append([homePitcher, hPID])

            awayPitcher = game["away_probable_pitcher"]
            # Get the player_id of the away pitcher
            aPID = lg.player_details(awayPitcher)[0]['player_id']
            # Add the awayPitcher's name and id to the list
            awayPIDList.append([awayPitcher, aPID])

        # For every home pitcher
        for i in homePIDList:
            # Get the pitchers stats over the last month if available, if not then just add player's name and id
            try:
                hPStats = League.getPitcher(self, "lastmonth", i[1])
                homePitcherStatList.append(hPStats)
            except:
                homePitcherStatList.append({i[0]: [i[1], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]})

        # Create a list to hold all of the info desired for homePitchers
        finalHPList = []
        for i in range(0, len(homePitcherStatList)):
            finalHPList.append(list(homePitcherStatList[i].items()))
            # FIP = print(finalHPList[i][0][1][6])

        print("Home Pitcher stats over the past month: ")
        # Create a sorted list based on the pitcher's FIP score in descending score
        sortedHP = sorted(finalHPList, key=lambda item: item[0][1][6])
        # Print every pitcher in the sorted list
        for i in range(0, len(sortedHP)):
            print("Team: " + str(hTList[i]) + " HP: " + str(homePIDList[i][0]))
            print("IP: " + str(sortedHP[i][0][1][2]) + " BF: " + str(sortedHP[i][0][1][3]) + " BB%: " + str(
                sortedHP[i][0][1][4]) + " K%: " + str(sortedHP[i][0][1][5]) + " FIP: " + str(
                sortedHP[i][0][1][6]) + " ERA: " + str(sortedHP[i][0][1][7]) + " WHIP: " + str(
                sortedHP[i][0][1][8]) + " K: " + str(sortedHP[i][0][1][10]) + " HR: " + str(sortedHP[i][0][1][11]))
            print("Note: " + str(hNList[i]))

        print("\n")

        # For every away pitcher
        for i in awayPIDList:
            # Get the pitchers stats over the last month if available, if not then just add player's name and id
            try:
                aPStats = League.getPitcher(self, "lastmonth", i[1])
                awayPitcherStatList.append(aPStats)
            except:
                awayPitcherStatList.append({i[0]: [i[1], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]})

        # Create a list to hold all of the info desired for awayPitchers
        finalAPList = []
        for i in range(0, len(awayPitcherStatList)):
            finalAPList.append(list(awayPitcherStatList[i].items()))
            # FIP = print(finalHPList[i][0][1][6])

        print("Away Pitcher stats over the past month: ")
        # Create a sorted list based on the pitcher's FIP score in descending score
        sortedAP = sorted(finalAPList, key=lambda item: item[0][1][6])
        # Print every pitcher in the sorted list
        for i in range(0, len(sortedAP)):
            print("Team: " + str(aTList[i]) + " AP: " + str(awayPIDList[i][0]))
            print("IP: " + str(sortedAP[i][0][1][2]) + " BF: " + str(sortedAP[i][0][1][3]) + " BB%: " + str(
                sortedAP[i][0][1][4]) + " K%: " + str(sortedAP[i][0][1][5]) + " FIP: " + str(
                sortedAP[i][0][1][6]) + " ERA: " + str(sortedHP[i][0][1][7]) + " WHIP: " + str(
                sortedAP[i][0][1][8]) + " K: " + str(sortedAP[i][0][1][10]) + " HR: " + str(sortedAP[i][0][1][11]))
            print("Note: " + str(aNList[i]))

        print("\nTeam batter stats over the past week: ")
        # Create a dict containing the stats of all batters on team over the past week
        teamBatters = League.getBatters(self, "lastweek", 3)
        # Print every batter in teamBatters
        League.printBatters(self, 'lastweek', teamBatters)

    def printBatters(self, type, passedDict):
        pass
        """
        Useful function to print a dict of batters that is passed, 'passedDict'
        :param type: Desired time for stats
        :param passedDict: Contains a dictionary of batters that need printed
        :return:
        """
        # Created a sorted list of batters, based on their WRC+ in descending order
        sortedBList = sorted(passedDict.items(), key=lambda item: item[1][9], reverse=True)
        for i in sortedBList:
            # If type equals 'season', print WAR. If it doesnt then dont include WAR since it cant be calculated
            if type == "season":
                print("Name: " + str(i[0]) + " PA: " + str(i[1][0]) + " wRC: " + str(
                    i[1][7]) + " wRC/PA: " + str(i[1][10]) + " wOBA: " + str(i[1][6]) + " BABIP: " + str(
                    i[1][3]) + " WAR: " + str(
                    i[1][8]) + " wRC+: " + str(i[1][9]))
            else:
                print("Name: " + str(i[0]) + " PA: " + str(i[1][0]) + " wRC: " + str(
                    i[1][7]) + " wRC/PA: " + str(i[1][10]) + " wOBA: " + str(i[1][6]) + " BABIP: " + str(
                    i[1][3]) + " wRC+: " + str(i[1][9]))

    def printPitchers(self, type, passedDict):
        pass
        """
        Useful function to print a dict of pitchers that is passed, 'passedDict'
        :param type: Desired time for stats
        :param passedDict: Contains a dictionary of pitchers that need printed
        :return:
        """
        # Created a sorted list of pitchers, based on their FIP in descending order
        sortedPList = sorted(passedDict.items(), key=lambda item: item[1][6])
        for i in sortedPList:
            # If type equals 'season', print WAR. If it doesnt then dont include WAR since it cant be calculated
            if type == "season":
                print("Name: " + str(i[0]) + " GS: " + str(i[1][1]) + " IP: " + str(
                    i[1][2]) + " BF: " + str(i[1][3]) + " BB%: " + str(i[1][4]) + " K%: " + str(
                    i[1][5]) + " FIP: " + str(i[1][6]) + " ERA: " + str(i[1][7]) + " WHIP: " + str(
                    i[1][8]) + " WAR: " + str(i[1][9]))
            else:
                print("Name: " + str(i[0]) + " GS: " + str(i[1][1]) + " IP: " + str(
                    i[1][2]) + " BF: " + str(i[1][3]) + " BB%: " + str(i[1][4]) + " K%: " + str(
                    i[1][5]) + " FIP: " + str(i[1][6]) + " ERA: " + str(i[1][7]) + " WHIP: " + str(
                    i[1][8]))

    def getBatters(self, type, status):
        pass
        """
        Function to query all batters giving the option for stat desired time range and what batters to include
        :param type: Desired timeline for stats
        :param status: 0 == all batters, 1 == rostered batters, 2 == free agent batters, 3 == batters currently on your team
        :return: dict of desired batters based on the given status
        """
        # Create lists to hold the player id's of your batters, FA batters, rostered batters, and all batters in the league
        faBID = []
        takenBID = []
        allBID = []
        teamBID = []

        # Create dicts to hold each batter, FA batter, rostered batter, and all batters in the league
        allBatterDict = {}
        takenBatterDict = {}
        faBatterDict = {}
        teamBatterDict = {}

        # Add every batter to allBID
        if status == 0:
            for i in lg.taken_players():
                if i["position_type"] == "B":
                    takenBID.append(i["player_id"])
            for i in lg.free_agents('B'):
                if i["position_type"] == "B":
                    faBID.append(i["player_id"])
            for i in tm.roster(lg.current_week()):
                if i["position_type"] == "B":
                    teamBID.append(i["player_id"])
            allBID.append(takenBID)
            allBID.append(faBID)
            allBID.append(teamBID)
        # Add every taken batter to allBID
        elif status == 1:
            for i in lg.taken_players():
                if i["position_type"] == "B":
                    takenBID.append(i["player_id"])
            allBID.append(takenBID)
        # Add every FA batter to allBID
        elif status == 2:
            for i in lg.free_agents('B'):
                if i["position_type"] == "B":
                    faBID.append(i["player_id"])
            allBID.append(faBID)
        # Add every batter on your team to allBID
        else:
            for i in tm.roster(lg.current_week()):
                if i["position_type"] == "B":
                    teamBID.append(i["player_id"])
            allBID.append(teamBID)

        # For every different list within allBID (up to 3: taken, fa, roster)
        for i in range(0, len(allBID)):
            # Get a list of batter stats given a list of player ids and the desired time range
            batterStats = lg.player_stats(allBID[i], req_type=type)
            # Get a list of all details for a batter, primarily used for their team to get their ballpark factor
            pD = lg.player_details(allBID[i])
            # For every batter in our current list
            for j in range(0, len(batterStats)):
                wOBA = 0
                BABIP = 0
                wRC = 0
                bb = 0
                k = 0

                playerName = batterStats[j]['name']
                playerID = batterStats[j]['player_id']

                # Get the players team from our pD object
                playerTeam = pD[j]['editorial_team_full_name']

                playerAB = batterStats[j]['AB']  # Number of player at-bats
                playerAVG = batterStats[j]['AVG']  # Player's batting average
                playerOPS = batterStats[j]['OPS']  # Player's OBP + Slugging
                playerHR = batterStats[j]['HR']  # Number of home runs hit
                playerRBI = batterStats[j]['RBI']  # Number of runs batted in
                playerR = batterStats[j]['R']  # Number of runs scored
                playerSB = batterStats[j]['SB']  # Number of stolen bases
                playerBB = batterStats[j]['BB']  # Number of walks
                playerIBB = batterStats[j]['IBB']  # Number of intentional walks
                playerSF = batterStats[j]['SF']  # Number of sacrifice flies
                playerHBP = batterStats[j]['HBP']  # Number of times hit by a pitch
                player1B = batterStats[j]['1B']  # Number of singles
                player2B = batterStats[j]['2B']  # Number of doubles
                player3B = batterStats[j]['3B']  # Number of triples
                playerPA = batterStats[j]['PA']  # Number of plate appearances
                playerSO = batterStats[j]['SO']  # Number of strikeouts
                playerH = batterStats[j]['H']  # Number of hits

                # Set every stat that is not available to 0.0
                if playerAB == "-": playerAB = 0
                if playerAVG == "-": playerAVG = 0
                if playerOPS == "-": playerOPS = 0
                if playerHR == "-": playerHR = 0
                if playerSB == "-": playerSB = 0
                if playerRBI == "-": playerRBI = 0
                if playerR == "-": playerR = 0
                if playerBB == "-": playerBB = 0
                if playerIBB == "-": playerIBB = 0
                if playerSF == "-": playerSF = 0
                if playerHBP == "-": playerHBP = 0
                if player1B == "-": player1B = 0
                if player2B == "-": player2B = 0
                if player3B == "-": player3B = 0
                if playerPA == "-": playerPA = 0
                if playerSO == "-": playerSO = 0
                if playerH == "-": playerH = 0

                # 2021 season constants for the NL and AL Weighted Runs Created and Plate Apperances
                alWRC = 4105
                alPA = 33304
                nlWRC = 4244
                nlPA = 33198

                # Set playerWar if type is season, otherwise set to 0 since it is not available
                try:
                    playerWAR = batterStats[j]['WAR']
                except:
                    playerWAR = 0

                if playerWAR == "-": playerWAR = 0

                # Gets the player's weighted on base average if available using league constants from FanGraphs
                try:
                    wOBA = ((.691 * float(playerBB)) + (.722 * float(playerHBP)) + (.883 * float(player1B)) + (
                                1.256 * float(player2B)) + (
                                    1.592 * float(player3B)) + (2.05 * float(playerHR))) / (
                                       playerAB + playerBB - playerIBB + playerSF + playerHBP)
                    wOBA = "{:.3f}".format(wOBA)
                except:
                    wOBA = 0

                # Get the player's batting average on balls in play
                try:
                    BABIP = (playerH - playerHR) / (playerAB - playerHR - playerSO + playerSF)
                    BABIP = "{:.3f}".format(BABIP)
                except:
                    BABIP = 0

                # Gets the player's number of weighted runs scored
                try:
                    wRC = (((float(wOBA) - .310) / 1.243) + .118) * float(playerPA)
                    wRC = "{:.3f}".format(wRC)
                except:
                    wRC = 0
                # Gets the player's number of weighted runs created per plate appearance
                try:
                    wRCPA = float(wRC) / float(playerPA)
                    wRCPA = "{:.3f}".format(wRCPA)
                except:
                    wRCPA = 0
                # Gets the player's weighted runs above average which gives us their weighted runs created plus which incorporates ballpark factors
                try:
                    wRAA = (float(wOBA) - .310) / 1.239
                    playerParkFactor = ballParkDict[playerTeam] / 100
                    if playerTeam in nlTeamList:
                        wRCP = ((((float(wRAA) / float(playerPA)) + .118) + (
                                    .118 - (float(playerParkFactor) * .118))) / (nlWRC / nlPA)) * 100
                    else:
                        wRCP = ((((float(wRAA) / float(playerPA)) + .118) + (
                                    .118 - (float(playerParkFactor) * .118))) / (alWRC / alPA)) * 100
                except:
                    wRAA = 0
                    wRCP = 0
                # Get the players walk and strikeout percentages
                try:
                    bb = (playerBB / playerAB) * 100
                    bb = "{:.3f}".format(bb)
                except:
                    bb = 0
                try:
                    k = (playerSO / playerAB) * 100
                    k = "{:.3f}".format(k)
                except:
                    k = 0
                # Add the player to their respective dictionary
                if status == 1:
                    takenBatterDict.update(
                        {playerName: [playerPA, float(bb), float(k), float(BABIP), float(playerAVG), float(playerOPS),
                                      float(wOBA), float(wRC), float(playerWAR), float(wRCP), float(wRCPA)]})
                elif status == 2:
                    faBatterDict.update(
                        {playerName: [playerPA, float(bb), float(k), float(BABIP), float(playerAVG), float(playerOPS),
                                      float(wOBA), float(wRC), float(playerWAR), float(wRCP), float(wRCPA)]})
                elif status == 3:
                    teamBatterDict.update(
                        {playerName: [playerPA, float(bb), float(k), float(BABIP), float(playerAVG), float(playerOPS),
                                      float(wOBA), float(wRC), float(playerWAR), float(wRCP), float(wRCPA)]})
        # Return dict of all batters in the league
        if status == 0:
            allBatterDict.update(takenBatterDict)
            allBatterDict.update(faBatterDict)
            allBatterDict.update(teamBatterDict)
            return allBatterDict
        # Return dict of all batters rostered
        elif status == 1:
            return takenBatterDict
        # Return dict of all batters currently a FA
        elif status == 2:
            return faBatterDict
        # Return a dict of all batters currently on the user's team
        else:
            return teamBatterDict

    def getBatter(self, type, playerID):
        pass
        # Get a list of batter stats given a player id and the desired time range
        batterStats = lg.player_stats(playerID, req_type=type)
        # Get a list of all details for a batter, primarily used for their team to get their ballpark factor
        pD = lg.player_details(playerID)
        wOBA = 0
        BABIP = 0
        wRC = 0
        bb = 0
        k = 0

        playerName = batterStats[0]['name']
        playerID = batterStats[0]['player_id']

        # Get the players team from our pD object
        playerTeam = pD[0]['editorial_team_full_name']

        playerAB = batterStats[0]['AB']  # Number of player at-bats
        playerAVG = batterStats[0]['AVG']  # Player's batting average
        playerOPS = batterStats[0]['OPS']  # Player's OBP + Slugging
        playerHR = batterStats[0]['HR']  # Number of home runs hit
        playerRBI = batterStats[0]['RBI']  # Number of runs batted in
        playerR = batterStats[0]['R']  # Number of runs scored
        playerSB = batterStats[0]['SB']  # Number of stolen bases
        playerBB = batterStats[0]['BB']  # Number of walks
        playerIBB = batterStats[0]['IBB']  # Number of intentional walks
        playerSF = batterStats[0]['SF']  # Number of sacrifice flies
        playerHBP = batterStats[0]['HBP']  # Number of times hit by a pitch
        player1B = batterStats[0]['1B']  # Number of singles
        player2B = batterStats[0]['2B']  # Number of doubles
        player3B = batterStats[0]['3B']  # Number of triples
        playerPA = batterStats[0]['PA']  # Number of plate appearances
        playerSO = batterStats[0]['SO']  # Number of strikeouts
        playerH = batterStats[0]['H']  # Number of hits

        # Set every stat that is not available to 0.0
        if playerAB == "-": playerAB = 0
        if playerAVG == "-": playerAVG = 0
        if playerOPS == "-": playerOPS = 0
        if playerHR == "-": playerHR = 0
        if playerSB == "-": playerSB = 0
        if playerRBI == "-": playerRBI = 0
        if playerR == "-": playerR = 0
        if playerBB == "-": playerBB = 0
        if playerIBB == "-": playerIBB = 0
        if playerSF == "-": playerSF = 0
        if playerHBP == "-": playerHBP = 0
        if player1B == "-": player1B = 0
        if player2B == "-": player2B = 0
        if player3B == "-": player3B = 0
        if playerPA == "-": playerPA = 0
        if playerSO == "-": playerSO = 0
        if playerH == "-": playerH = 0

        # 2021 season constants for the NL and AL Weighted Runs Created and Plate Apperances
        alWRC = 4105
        alPA = 33304
        nlWRC = 4244
        nlPA = 33198

        # Set playerWar if type is season, otherwise set to 0 since it is not available
        try:
            playerWAR = batterStats[0]['WAR']
        except:
            playerWAR = 0

        if playerWAR == "-": playerWAR = 0

        # Gets the player's weighted on base average if available using league constants from FanGraphs
        try:
            wOBA = ((.691 * float(playerBB)) + (.722 * float(playerHBP)) + (.883 * float(player1B)) + (
                    1.256 * float(player2B)) + (
                            1.592 * float(player3B)) + (2.05 * float(playerHR))) / (
                           playerAB + playerBB - playerIBB + playerSF + playerHBP)
            wOBA = "{:.3f}".format(wOBA)
        except:
            wOBA = 0

        # Get the player's batting average on balls in play
        try:
            BABIP = (playerH - playerHR) / (playerAB - playerHR - playerSO + playerSF)
            BABIP = "{:.3f}".format(BABIP)
        except:
            BABIP = 0

        # Gets the player's number of weighted runs scored
        try:
            wRC = (((float(wOBA) - .310) / 1.243) + .118) * float(playerPA)
            wRC = "{:.3f}".format(wRC)
        except:
            wRC = 0
        # Gets the player's number of weighted runs created per plate appearance
        try:
            wRCPA = float(wRC) / float(playerPA)
            wRCPA = "{:.3f}".format(wRCPA)
        except:
            wRCPA = 0
        # Gets the player's weighted runs above average which gives us their weighted runs created plus which incorporates ballpark factors
        try:
            wRAA = (float(wOBA) - .310) / 1.239
            playerParkFactor = ballParkDict[playerTeam] / 100
            if playerTeam in nlTeamList:
                wRCP = ((((float(wRAA) / float(playerPA)) + .118) + (.118 - (float(playerParkFactor) * .118))) / (
                        nlWRC / nlPA)) * 100
            else:
                wRCP = ((((float(wRAA) / float(playerPA)) + .118) + (.118 - (float(playerParkFactor) * .118))) / (
                        alWRC / alPA)) * 100
        except:
            wRAA = 0
            wRCP = 0
        # Get the players walk and strikeout percentages
        try:
            bb = (playerBB / playerAB) * 100
            bb = "{:.3f}".format(bb)
        except:
            bb = 0
        try:
            k = (playerSO / playerAB) * 100
            k = "{:.3f}".format(k)
        except:
            k = 0
        # Return the desired player
        return {
            playerName: [playerPA, float(bb), float(k), float(BABIP), float(playerAVG), float(playerOPS), float(wOBA),
                         float(wRC), float(playerWAR), float(wRCP), float(wRCPA)]}

    def getPitcher(self, type, playerID):
        pass
        """
        Function to query a pitcher given an id, with the option for stat desired time range
        :param type: Desired timeline for stats
        :return: desired pitcher's stats in the form of a dict
        """
        # Get a list of pitcher stats given player's id and the desired time range
        pitcherStats = lg.player_stats(playerID, req_type=type)
        playerName = pitcherStats[0]['name']
        playerID = pitcherStats[0]['player_id']
        playerGames = pitcherStats[0]['G']
        playerIP = pitcherStats[0]['IP']

        playerBF = pitcherStats[0]['BF']  # Number of batters faced
        playerBB = pitcherStats[0]['BB']  # Number of batters walked
        playerKP = pitcherStats[0]['K']  # Number of strikeouts
        playerHGU = pitcherStats[0]['H']  # Number of hits allowed
        playerHR = pitcherStats[0]['HR']  # Number of home runs allowed
        playerHBP = pitcherStats[0]['HBP']  # Number of batters hit with a pitch
        playerERA = pitcherStats[0]['ERA']  # Player's ERA
        playerWHIP = pitcherStats[0]['WHIP']  # Player's WHIP

        try:
            playerWAR = pitcherStats[0]['WAR']
        except:
            playerWAR = 0

        # Set every stat that is not available to 0.0
        if playerBF == "-":
            playerBF = 0
        if playerBB == "-":
            playerBB = 0
        if playerKP == "-":
            playerKP = 0
        if playerHGU == "-":
            playerHGU = 0
        if playerHR == "-":
            playerHR = 0
        if playerHBP == "-":
            playerHBP = 0
        if playerIP == "-":
            playerIP = 0
        if playerWAR == "-":
            playerWAR = 0

        # Set strikeouts before it is modified for K%
        strikeouts = playerKP

        # Get the metrics that require division by batters faced
        try:
            playerHGU /= playerBF
        except:
            playerHGU = 0

        try:
            bb = float(playerBB) / float(playerBF)
        except:
            bb = 0

        try:
            kP = float(playerKP) / float(playerBF)
        except:
            kP = 0

        # Multiply BB and KP by 100 to get a percentage and format them
        bb *= 100
        kP *= 100
        bb = "{:.2f}".format(bb)
        kP = "{:.2f}".format(kP)
        playerHGU = "{:.2f}".format(playerHGU)

        # Calculate the FIP score if possible
        try:
            FIP = (13 * float(playerHR) + 3 * (float(playerBB) + float(playerHBP)) - 2 * strikeouts) / float(
                playerIP)
            # Constant is the league average FPI score for 2021
            FIP_constant = 3.133
            FIP += FIP_constant
        except:
            FIP = 0

        FIP = "{:.2f}".format(FIP)

        # Return the desired pitcher
        return {
            playerName: [float(playerID), float(playerGames), float(playerIP), float(playerBF), float(bb), float(kP),
                         float(FIP), float(playerERA), float(playerWHIP), float(playerWAR), float(strikeouts),
                         float(playerHR)]}

    def getPitchers(self, type, status):
        pass
        """
        Function to query all pitchers giving the option for stat desired time range and what pitchers to include
        :param type: Desired timeline for stats
        :param status: 0 == all pitchers, 1 == rostered pitchers, 2 == free agent pitchers, 3 == pitchers currently on your team
        :return: dict of desired pitchers based on the given status
        """
        # Create lists to hold the player id's of your pitchers, FA pitchers, rostered pitchers, and all pitchers in the league
        faPID = []
        takenPID = []
        allPID = []
        teamPID = []

        # Create dicts to hold each pitcher, FA pitcher, rostered pitcher, and all pitchers in the league
        allPitcherDict = {}
        takenPlayerPDict = {}
        fAPitcherDict = {}
        teamPitcherDict = {}

        # Add every batter to allPID
        if status == 0:
            for i in lg.taken_players():
                if i["position_type"] == "P":
                    takenPID.append(i["player_id"])
            for i in lg.free_agents('P'):
                if i["position_type"] == "P":
                    faPID.append(i["player_id"])
            for i in tm.roster(lg.current_week()):
                if i["position_type"] == "P":
                    teamPID.append(i["player_id"])
            allPID.append(takenPID)
            allPID.append(faPID)
            allPID.append(teamPID)
        # Add every taken pitcher to allPID
        elif status == 1:
            for i in lg.taken_players():
                if i["position_type"] == "P":
                    takenPID.append(i["player_id"])
            allPID.append(takenPID)
        # Add every FA pitcher to allPID
        elif status == 2:
            for i in lg.free_agents('P'):
                if i["position_type"] == "P":
                    faPID.append(i["player_id"])
            allPID.append(faPID)
        # Add every pitcher on your team to allPID
        else:
            for i in tm.roster(lg.current_week()):
                if i["position_type"] == "P":
                    teamPID.append(i["player_id"])
            allPID.append(teamPID)

        # For every different list within allPID (up to 3: taken, fa, roster)
        for i in range(0, len(allPID)):
            # Get a list of pitcher stats given a list of player ids and the desired time range
            pitcherStats = lg.player_stats(allPID[i], req_type=type)
            for j in range(0, len(pitcherStats)):
                playerName = pitcherStats[j]['name']
                playerID = pitcherStats[j]['player_id']
                playerGames = pitcherStats[j]['G']
                playerIP = pitcherStats[j]['IP']

                playerBF = pitcherStats[j]['BF']  # Number of batters faced
                playerBB = pitcherStats[j]['BB']  # Number of batters walked
                playerKP = pitcherStats[j]['K']  # Number of strikeouts
                playerHGU = pitcherStats[j]['H']  # Number of hits allowed
                playerHR = pitcherStats[j]['HR']  # Number of home runs allowed
                playerHBP = pitcherStats[j]['HBP']  # Number of batters hit with a pitch
                playerERA = pitcherStats[j]['ERA']  # Player's ERA
                playerWHIP = pitcherStats[j]['WHIP']  # Player's WHIP

                try:
                    playerWAR = pitcherStats[j]['WAR']
                except:
                    playerWAR = 0

                # Set every stat that is not available to 0.0
                if playerBF == "-":
                    playerBF = 0
                if playerBB == "-":
                    playerBB = 0
                if playerKP == "-":
                    playerKP = 0
                if playerHGU == "-":
                    playerHGU = 0
                if playerHR == "-":
                    playerHR = 0
                if playerHBP == "-":
                    playerHBP = 0
                if playerIP == "-":
                    playerIP = 0
                if playerWAR == "-":
                    playerWAR = 0

                # Set strikeouts before it is modified for K%
                strikeouts = playerKP

                # Get the metrics that require division by batters faced
                try:
                    playerHGU /= playerBF
                except:
                    playerHGU = 0

                try:
                    bb = float(playerBB) / float(playerBF)
                except:
                    bb = 0

                try:
                    kP = float(playerKP) / float(playerBF)
                except:
                    kP = 0

                # Multiply BB and KP by 100 to get a percentage and format them
                bb *= 100
                kP *= 100
                bb = "{:.2f}".format(bb)
                kP = "{:.2f}".format(kP)
                playerHGU = "{:.2f}".format(playerHGU)

                # Calculate the FIP score if possible
                try:
                    FIP = (13 * float(playerHR) + 3 * (float(playerBB) + float(playerHBP)) - 2 * strikeouts) / float(
                        playerIP)
                    # Constant is the league average FPI score for 2021
                    FIP_constant = 3.133
                    FIP += FIP_constant
                except:
                    FIP = 0

                FIP = "{:.2f}".format(FIP)
                # Add the player to their respective dictionary
                if status == 1:
                    takenPlayerPDict.update(
                        {playerName: [playerID, playerGames, playerIP, playerBF, bb, kP, FIP, playerERA, playerWHIP,
                                      playerWAR, strikeouts, playerHR]})
                elif status == 2:
                    fAPitcherDict.update(
                        {playerName: [playerID, playerGames, playerIP, playerBF, bb, kP, FIP, playerERA, playerWHIP,
                                      playerWAR, strikeouts, playerHR]})
                elif status == 3:
                    teamPitcherDict.update(
                        {playerName: [playerID, playerGames, playerIP, playerBF, bb, kP, FIP, playerERA, playerWHIP,
                                      playerWAR, strikeouts, playerHR]})
        # Return dict of all pitchers in the league
        if status == 0:
            allPitcherDict.update(takenPlayerPDict)
            allPitcherDict.update(fAPitcherDict)
            allPitcherDict.update(teamPitcherDict)
            return allPitcherDict
        # Return dict of all pitchers rostered
        elif status == 1:
            return takenPlayerPDict
        # Return dict of all pitchers currently a FA
        elif status == 2:
            return fAPitcherDict
        # Return a dict of all pitchers currently on the user's team
        else:
            return teamPitcherDict

    def getAllPlayers(self, type):
        pass
        teamPitchers = League.getPitchers(self, type, 3)
        print("All pitchers currently on your team:")
        League.printPitchers(self, type, teamPitchers)

        takenPitchers = League.getPitchers(self, type, 1)
        print("All pitchers currently on teams:")
        League.printPitchers(self, type, takenPitchers)

        faPitchers = League.getPitchers(self, type, 2)
        print("All free-agent pitchers")
        League.printPitchers(self, type, faPitchers)

        teamBatters = League.getBatters(self, type, 3)
        print("All batters currently on your team:")
        League.printBatters(self, type, teamBatters)

        takenBatters = League.getBatters(self, type, 1)
        print("All batters currently on teams:")
        League.printBatters(self, type, takenBatters)

        faBatters = League.getBatters(self, type, 2)
        print("All free-agent batters")
        League.printBatters(self, type, faBatters)




