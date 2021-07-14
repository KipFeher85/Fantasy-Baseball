# This is a sample Python script.

from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
import statsapi
import csv
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta


class League:
    # Obtain Yahoo OAuth2 access token from the file given
    oauth = OAuth2(None, None, from_file='OAuth2.json')

    # Create a Yahoo Fantasy MLB Game object using the access token
    gm = yfa.Game(oauth, 'mlb')

    # Get the league id desired
    leagueID = gm.league_ids(year=2021)[0]

    # Create a league object given the first id of the user's league id's for the season
    lg = gm.to_league(leagueID)

    # Create a team object given the team's key
    tm = lg.to_team(team_key=lg.team_key())

    # Create dict to hold ballpark factors, lists to hold NL and AL team names
    ballParkDict = {}
    alTeamList = []
    nlTeamList = []

    obaW = 0
    wOBAScale = 0
    wBB = 0
    wHBP = 0
    w1B = 0
    w2B = 0
    w3B = 0
    wHR = 0
    rPAW = 0  # wRAA weight

    alPA = 0
    alWRC = 0
    nlPA = 0
    nlWRC = 0

    FIP_Constant = 0

    @staticmethod
    def update_league_constants():
        """
        THIS FUNCTION ONLY NEEDS TO BE CALLED ONCE PER DAY
        This function allows the user to not exceed the rate-limit for any api

        Gets the following weights for the season from fangraphs:
        - OBA, wOBA Scale, wBB, wHBP, w1B, w2B, w3B, wHR, wRAA weight
        Gets PA and WRC stats for both NL and AL over the following time periods:
        - Season, Last Month (From the current day), Last Week (From the current day)

        Writes this data to a csv file 'leagueConstants.csv'
        :return:
        """

        # Url for the fangraphs 'GUTS' page
        gutsURL = "https://www.fangraphs.com/guts.aspx?type=cn"
        # Turn the html page into a dataframe
        gutsDF = pd.read_html(gutsURL)[8].loc[0]

        # Set the League object's weights
        League.obaW = gutsDF[1]
        League.wOBAScale = gutsDF[2]
        League.wBB = gutsDF[3]
        League.wHBP = gutsDF[4]
        League.w1B = gutsDF[5]
        League.w2B = gutsDF[6]
        League.w3B = gutsDF[7]
        League.wHR = gutsDF[8]
        League.rPAW = gutsDF[11]  # wRAA weight
        League.FIP_Constant = gutsDF[13]

        # Create a list to hold the urls for NL and AL stats over different time periods
        alURList = []
        nlURList = []

        # Get today's date
        month = date.today().strftime("%m")
        day = date.today().strftime("%d")
        year = "20" + date.today().strftime("%y")

        # Set the url to get AL and NL league stats for the season
        alURList.append("https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=al&qual=0&type=1&season=2021&month=1000&season1=2021&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate=2021-01-01&enddate=" + str(
                year) + "-" + str(month) + "-" + str(day))
        nlURList.append("https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=nl&qual=0&type=1&season=2021&month=1000&season1=2021&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate=2021-01-01&enddate=" + str(
                year) + "-" + str(month) + "-" + str(day))

        # Get the date of previous month from current day
        last_month = date.today() - relativedelta(months=1)
        lMonth = last_month.strftime("%m")
        lDay = last_month.strftime("%d")
        lYear = "20" + last_month.strftime("%y")

        # Set the url to get AL and NL league stats for the last month
        alURList.append("https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=al&qual=0&type=1&season=2021&month=1000&season1=2021&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate=" + str(
                lYear) + "-" + str(lMonth) + "-" + str(lDay) + "&enddate=" + str(
                year) + "-" + str(month) + "-" + str(day))
        nlURList.append("https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=nl&qual=0&type=1&season=2021&month=1000&season1=2021&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate=" + str(
                lYear) + "-" + str(lMonth) + "-" + str(lDay) + "&enddate=" + str(
                year) + "-" + str(month) + "-" + str(day))

        # Get the date of previous week from current day
        last_week = date.today() - relativedelta(weeks=1)
        lMonth = last_week.strftime("%m")
        lDay = last_week.strftime("%d")
        lYear = "20" + last_week.strftime("%y")

        # Set the url to get AL and NL league stats for the last month
        alURList.append("https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=al&qual=0&type=1&season=2021&month=1000&season1=2021&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate=" + str(
                lYear) + "-" + str(lMonth) + "-" + str(lDay) + "&enddate=" + str(
                year) + "-" + str(month) + "-" + str(day))
        nlURList.append("https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=nl&qual=0&type=1&season=2021&month=1000&season1=2021&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate=" + str(
                lYear) + "-" + str(lMonth) + "-" + str(lDay) + "&enddate=" + str(
                year) + "-" + str(month) + "-" + str(day))

        # Create lists to hold AL and NL league stats
        alPAList = []
        alWRCList = []
        nlPAList = []
        nlWRCList = []

        # For every different time period
        for i in range(0, len(alURList)):
            # Create the unique data frame
            alDF = pd.read_html(alURList[i])[16]
            nlDF = pd.read_html(nlURList[i])[16]

            # Add contents to a respective list
            alPAList.append(alDF.loc[0][2])
            alWRCList.append(alDF.loc[0][16])
            nlPAList.append(nlDF.loc[0][2])
            nlWRCList.append(nlDF.loc[0][16])

        # Open csv file and create a file object
        with open('leagueConstants.csv', mode='w') as league_file:
            league_writer = csv.writer(league_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # Write data to the csv files
            league_writer.writerow(['Time', 'Season', 'Last Month', 'Last Week'])
            league_writer.writerow(['OBA Weight', League.obaW])
            league_writer.writerow(['wOBA Scale', League.wOBAScale])
            league_writer.writerow(['BB Weight', League.wBB])
            league_writer.writerow(['HBP Weight', League.wHBP])
            league_writer.writerow(['1B Weight', League.w1B])
            league_writer.writerow(['2B Weight', League.w2B])
            league_writer.writerow(['3B Weight', League.w3B])
            league_writer.writerow(['HR Weight', League.wHR])
            league_writer.writerow(['wRAA Weight', League.rPAW])
            league_writer.writerow(['AL Plate Appearances', alPAList[0], alPAList[1], alPAList[2]])
            league_writer.writerow(['AL Weighted Runs Created', alWRCList[0], alWRCList[1], alWRCList[2]])
            league_writer.writerow(['NL Plate Appearances', nlPAList[0], nlPAList[1], nlPAList[2]])
            league_writer.writerow(['NL Weighted Runs Created', nlWRCList[0], nlWRCList[1], nlWRCList[2]])
            league_writer.writerow(['FIP Constant', League.FIP_Constant])

    @staticmethod
    def starter():
        """
        Initializes the league object, needs to be always be called
        - Gets list of NL and AL teams in addition to each ball park factor
        - Grabs the season FIP constant from 'leagueConstants.csv'
        :return:
        """

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
            League.ballParkDict.update({teamList[i]: bfList[i]})
        # Add every AL team to a list
        for i in range(0, 14):
            League.alTeamList.append(teamList[i])
        # Add every NL team to a list
        for i in range(14, len(teamList)):
            League.nlTeamList.append(teamList[i])
        # Add a column to the dict for both the NL and AL avg ballpark factor
        League.ballParkDict.update({"NL Avg": data[0]['NL Basic']})
        League.ballParkDict.update({"AL Avg": data[0]['AL Basic']})

        # Open csv file
        df = pd.read_csv("leagueConstants.csv")
        # Get the 'Season' column from the data frame
        season = df.Season
        # Set the league's FIP constant
        League.FIP_Constant = season.loc[13]

    @staticmethod
    def get_player(player_name, time):
        """
        Returns a player's stats over the specified time period given a name
        :param player_name: str
        :param time: str - "season" || "lastmonth" || "lastweek"
        :return: Dict
        """
        playerDict = {}
        try:
            # Grab the player's id and position
            playerId = League.lg.player_details(player_name)[0]['player_id']
            playerPos = League.lg.player_details(player_name)[0]['position_type']

            # If player is a batter
            if playerPos == 'B':
                # Get the player's stats as a dict
                playerDict = League.get_batter(time, playerId)
                # Print the desired batter
            elif playerPos == 'P':
                playerDict = League.get_pitcher(time, playerId)
            return playerDict
        except:
            # If player is not available display message
            return str(player_name) + "'s stats not available"

    @staticmethod
    def print_player(player_name, time):
        """
        Display's the desired player's stats over the desired time period
        :param player_name: str - Player name
        :param time: str - "season" || "lastmonth" || "lastweek"
        :return:
        """
        # If player is a batter
        playerDict = League.get_player(player_name, time)
        if playerDict != str(player_name) + "'s stats not available":
            playerPos = League.lg.player_details(player_name)[0]['position_type']
            if playerPos == 'B':
                # Print the desired batter
                League.print_batters(playerDict, reverse=True)
            elif playerPos == 'P':
                League.print_pitchers(playerDict, reverse=False)
        else:
            # If player is not available display message
            print(playerDict)

    @staticmethod
    def current_roster_stats(time):
        """
        Display roster and their advanced stats over the desired time period
        :param time: str - "season" || "lastmonth" || "lastweek"
        :return:
        """
        print("Your batters: ")
        # Get the dict of all batters currently on your team
        currentBatters = League.get_batters(time, 3, False)
        # Print every batter and their advanced stats in currentBatters
        League.print_batters(currentBatters, True)

        print("\n" + "Your pitchers: ")
        # Get the dict of all pitchers currently on your team
        currentPitchers = League.get_pitchers(time, 3, False)
        # Print every pitcher and their advanced stats in currentPitchers
        League.print_pitchers(currentPitchers, False)

    @staticmethod
    def current_roster_basic():
        """
        Display's a player's entire roster without their stats but player details (Player Id, Position, Eligible Postions, Status)
        :return:
        """
        hitterList = []
        pitcherList = []
        injuredList = []

        # Iterate through every player on the team within the current week
        for i in League.tm.roster(League.lg.current_week()):
            if i["status"] != '':
                injuredList.append(i)
            elif i["position_type"] == 'P':
                pitcherList.append(i)
            else:
                hitterList.append(i)

        print("Hitter List: ")
        for i in hitterList:
            print(i)
        print("\n" + "Pitcher List: ")
        for i in pitcherList:
            print(i)
        print("\n" + "I, DTD, NA: ")
        for i in injuredList:
            print(i)

    @staticmethod
    def team_details():
        """
        Gives basic details for every team in the league including name, owner, owner legacy, logo info
        :return:
        """
        # Get dict of all teams in the league
        tms = League.lg.teams()
        for i in tms:
            print(list(tms[i].items()))

    @staticmethod
    def predict_team_day():
        """
        Function to help aid in the selection of players for the daily lineup
        Displays the probable pitchers for every game
        Probable pitcher's name, pregame note, and advanced stats from their past month are shown
        User's batter and pitcher advanced stats over the past week are displayed as well
        :return:
        """
        # Create a dictionary of all the games being played today
        today = statsapi.schedule(date="2021-07-01")
        if(len(today)) > 0:
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

                hN = game["home_pitcher_note"]
                aN = game["away_pitcher_note"]
                if hN == "":
                    hN = "Not Available"
                if aN == "":
                    aN = "Not Available"

                hNList.append(hN)
                aNList.append(aN)

                homePitcher = game["home_probable_pitcher"]
                # Get the player_id of the home pitcher
                try:
                    hPID = League.lg.player_details(homePitcher)[0]['player_id']
                except:
                    hPID = 0
                # Add the homePitcher's name and id to the list
                homePIDList.append([homePitcher, hPID])

                awayPitcher = game["away_probable_pitcher"]
                # Get the player_id of the away pitcher
                try:
                    aPID = League.lg.player_details(awayPitcher)[0]['player_id']
                except:
                    aPID = 0
                # Add the awayPitcher's name and id to the list
                awayPIDList.append([awayPitcher, aPID])

            # For every home pitcher
            for i in homePIDList:
                # Get the pitchers stats over the last month if available, if not then just add player's name and id
                try:
                    hPStats = League.get_pitcher("lastmonth", i[1])
                    homePitcherStatList.append(hPStats)
                except:
                    homePitcherStatList.append({i[0]: [i[1], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]})

            # Create a list to hold all of the info desired for homePitchers
            finalHPList = []
            for i in range(0, len(homePitcherStatList)):
                finalHPList.append(list(homePitcherStatList[i].items()))
                finalHPList.append(list(homePitcherStatList[i].items()))
                # FIP = print(finalHPList[i][0][1][6])

            # For every away pitcher
            for i in awayPIDList:
                # Get the pitchers stats over the last month if available, if not then just add player's name and id
                try:
                    aPStats = League.get_pitcher("lastmonth", i[1])
                    awayPitcherStatList.append(aPStats)
                except:
                    awayPitcherStatList.append({i[0]: [i[1], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]})

            # Create a list to hold all of the info desired for awayPitchers
            finalAPList = []
            for i in range(0, len(awayPitcherStatList)):
                finalAPList.append(list(awayPitcherStatList[i].items()))
                # FIP = print(finalHPList[i][0][1][6])

            for i in range(0, len(today)):
                print("\nGame " + str(i + 1) + ": " + str(aTList[i]) + " at " + str(hTList[i]))
                print("Pitcher Stats over the past month")
                print("HP: " + str(homePIDList[i][0]) + " IP: " + str(finalHPList[i][0][1][2]) + " BF: " + str(finalHPList[i][0][1][3]) + " BB%: " + str(
                    finalHPList[i][0][1][4]) + " K%: " + str(finalHPList[i][0][1][5]) + " FIP: " + str(
                    finalHPList[i][0][1][6]) + " ERA: " + str(finalHPList[i][0][1][7]) + " WHIP: " + str(
                    finalHPList[i][0][1][8]) + " K: " + str(finalHPList[i][0][1][10]) + " HR: " + str(finalHPList[i][0][1][11]))
                print(str(homePIDList[i][0]) + " Note: " + str(hNList[i]))
                print("AP: " + str(awayPIDList[i][0]) + " IP: " + str(finalAPList[i][0][1][2]) + " BF: " + str(finalAPList[i][0][1][3]) + " BB%: " + str(
                    finalAPList[i][0][1][4]) + " K%: " + str(finalAPList[i][0][1][5]) + " FIP: " + str(
                    finalAPList[i][0][1][6]) + " ERA: " + str(finalAPList[i][0][1][7]) + " WHIP: " + str(
                    finalAPList[i][0][1][8]) + " K: " + str(finalAPList[i][0][1][10]) + " HR: " + str(finalAPList[i][0][1][11]))
                print(str(awayPIDList[i][0]) + " Note: " + str(aNList[i]))
        else:
            print("There are no games today :/")

        print("\nTeam batter stats over the past week: ")
        # Create a dict containing the stats of all batters on team over the past week
        teamBatters = League.get_batters("lastweek", 3, qualified=False)
        # Print every batter in teamBatters
        League.print_batters(teamBatters, reverse=True)

        print("\nTeam pitcher stats over the past week: ")
        # Create a dict containing the stats of all pitchers on team over the past week
        teamPitchers = League.get_pitchers("lastweek", 3, qualified=False)
        # Print every batter in teamPitchers
        League.print_pitchers(teamPitchers, reverse=False)

    @staticmethod
    def print_batters(passed_dict, reverse):
        """
        Useful function to print a dict of batters that is passed, 'passedDict'
        :param passed_dict: Dict - Contains a dictionary of batters that need printed
        :param reverse: bool - True: Desc, False: Asc
        :return:
        """
        valueLength = len(list(passed_dict.values())[0])
        # If passed_dict contains WAR or list length is 11, print with WAR
        if valueLength == 11:
            # Created a sorted list of batters, based on their WRC+ in descending order
            sortedBList = sorted(passed_dict.items(), key=lambda item: item[1][9], reverse=reverse)
            for i in sortedBList:
                playerStats = i[1]
                # If WAR is available, print WAR. If it doesnt then dont include WAR since it cant be calculated
                print("Name: " + str(i[0]) + " PA: " + str(playerStats[0]) + " wRC: " + str(
                    playerStats[7]) + " wRC/PA: " + str(playerStats[10]) + " wOBA: " + str(playerStats[6]) + " BABIP: " + str(
                    playerStats[3]) + " WAR: " + str(playerStats[8]) + " wRC+: " + str(playerStats[9]))
        else:
            sortedBList = sorted(passed_dict.items(), key=lambda item: item[1][8], reverse=reverse)
            for i in sortedBList:
                playerStats = i[1]
                print("Name: " + str(i[0]) + " PA: " + str(playerStats[0]) + " wRC: " + str(
                    playerStats[7]) + " wRC/PA: " + str(playerStats[9]) + " wOBA: " + str(playerStats[6]) + " BABIP: " + str(
                    playerStats[3]) + " wRC+: " + str(playerStats[8]))

    @staticmethod
    def print_pitchers(passed_dict, reverse):
        """
        Useful function to print a dict of pitchers that is passed, 'passedDict'
        :param passed_dict: Dict - Contains a dictionary of pitchers that need printed
        :param reverse: bool - True: Desc, False: Asc
        :return:
        """
        sortedPList = sorted(passed_dict.items(), key=lambda item: item[1][6], reverse=reverse)
        # Created a sorted list of pitchers, based on their FIP in descending order
        for i in sortedPList:
            playerStats = i[1]
            if len(playerStats) == 15:
                # If type equals 'season', print WAR. If it doesnt then dont include WAR since it cant be calculated
                print("Name: " + str(i[0]) + " GS: " + str(playerStats[1]) + " IP: " + str(
                    playerStats[2]) + " BF: " + str(playerStats[3]) + " BB%: " + str(playerStats[4]) + " K%: " + str(
                    playerStats[5]) + " FIP: " + str(playerStats[6]) + " ERA: " + str(playerStats[7]) + " WHIP: " + str(
                    playerStats[8]) + " WAR: " + str(playerStats[9]) + " W: " + str(playerStats[12]) + " L: " + str(playerStats[13]) + " SV: " + str(playerStats[14]))
            else:
                print("Name: " + str(i[0]) + " GS: " + str(playerStats[1]) + " IP: " + str(
                    playerStats[2]) + " BF: " + str(playerStats[3]) + " BB%: " + str(playerStats[4]) + " K%: " + str(
                    playerStats[5]) + " FIP: " + str(playerStats[6]) + " ERA: " + str(playerStats[7]) + " WHIP: " + str(playerStats[8]) + " W: " + str(playerStats[11]) + " L: " + str(playerStats[12]) + " SV: " + str(playerStats[13]))

    @staticmethod
    def get_batters(time, status, qualified):
        """
        Function to query all batters giving the option for stat desired time range and what batters to include
        :param time: str - "season" || "lastmonth" || "lastweek"
        :param status: int - 0 == all batters, 1 == rostered batters, 2 == free agent batters, 3 == batters currently on your team
        :param qualified: bool - Whether or not to include only 'qualified' hitters
        based on the time period selected
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
            for i in League.lg.taken_players():
                if i["position_type"] == "B":
                    takenBID.append(i["player_id"])
            for i in League.lg.free_agents('B'):
                    faBID.append(i["player_id"])
            for i in League.tm.roster(League.lg.current_week()):
                if i["position_type"] == "B":
                    teamBID.append(i["player_id"])
            allBID.append(takenBID)
            allBID.append(faBID)
            allBID.append(teamBID)
        # Add every taken batter to allBID
        elif status == 1:
            for i in League.lg.taken_players():
                if i["position_type"] == "B":
                    takenBID.append(i["player_id"])
            allBID.append(takenBID)
        # Add every FA batter to allBID
        elif status == 2:
            for i in League.lg.free_agents('B'):
                if i["position_type"] == "B":
                    faBID.append(i["player_id"])
            allBID.append(faBID)
        # Add every batter on your team to allBID
        else:
            for i in League.tm.roster(League.lg.current_week()):
                if i["position_type"] == "B":
                    teamBID.append(i["player_id"])
            allBID.append(teamBID)

        # Read in leagueConstants as a data frame
        df = pd.read_csv("leagueConstants.csv")
        # Get the 'Season', 'Last Month', and 'Last Week' columns of the data frame
        season = df.Season
        lastmonth = df['Last Month']
        lastweek = df['Last Week']

        # Get the season weights
        League.obaW = season.loc[0]
        League.wOBAScale = season.loc[1]
        League.wBB = season.loc[2]
        League.wHBP = season.loc[3]
        League.w1B = season.loc[4]
        League.w2B = season.loc[5]
        League.w3B = season.loc[6]
        League.wHR = season.loc[7]
        League.rPAW = season.loc[8]

        # Set the AL and NL PA/WRC stats based on the time period
        if time == "season":
            League.alPA = season.loc[9]
            League.alWRC = season.loc[10]
            League.nlPA = season.loc[11]
            League.nlWRC = season.loc[12]
        elif time == "lastmonth":
            League.alPA = lastmonth.loc[9]
            League.alWRC = lastmonth.loc[10]
            League.nlPA = lastmonth.loc[11]
            League.nlWRC = lastmonth.loc[12]
        else:
            League.alPA = lastweek.loc[9]
            League.alWRC = lastweek.loc[10]
            League.nlPA = lastweek.loc[11]
            League.nlWRC = lastweek.loc[12]

        # Determine whether or not the qualifier is used
        if qualified == True:
            if time == "season":
                paQualifier = 150
            elif time == "lastmonth":
                paQualifier = 30
            else:
                paQualifier = 5
        else:
            paQualifier = 0

        # For every different list within allBID (up to 3: taken, fa, roster)
        for i in range(0, len(allBID)):
            # Get a list of batter stats given a list of player ids and the desired time range
            batterStats = League.lg.player_stats(allBID[i], req_type=time)
            # Get a list of all details for a batter, primarily used for their team to get their ballpark factor
            pD = League.lg.player_details(allBID[i])
            # For every batter in our current list
            for j in range(0, len(batterStats)):
                playerName = batterStats[j]['name']
                # playerID = batterStats['player_id']

                # Get the players team from our pD object
                playerTeam = pD[j]['editorial_team_full_name']

                playerAB = batterStats[j]['AB']  # Number of player at-bats
                playerPA = batterStats[j]['PA']  # Number of plate appearances
                if playerPA == "-": playerPA = 0

                if float(int(playerPA)) > paQualifier:
                    playerAVG = batterStats[j]['AVG']  # Player's batting average
                    playerOPS = batterStats[j]['OPS']  # Player's OBP + Slugging
                    playerHR = batterStats[j]['HR']  # Number of home runs hit

                    # playerRBI = batterStats['RBI']  # Number of runs batted in
                    # playerR = batterStats['R']  # Number of runs scored
                    # playerSB = batterStats['SB']  # Number of stolen bases

                    playerBB = batterStats[j]['BB']  # Number of walks
                    playerIBB = batterStats[j]['IBB']  # Number of intentional walks
                    playerSF = batterStats[j]['SF']  # Number of sacrifice flies
                    playerHBP = batterStats[j]['HBP']  # Number of times hit by a pitch
                    player1B = batterStats[j]['1B']  # Number of singles
                    player2B = batterStats[j]['2B']  # Number of doubles
                    player3B = batterStats[j]['3B']  # Number of triples
                    playerSO = batterStats[j]['SO']  # Number of strikeouts
                    playerH = batterStats[j]['H']  # Number of hits

                    # Set every stat that is not available to 0.0
                    if playerAB == "-": playerAB = 0
                    if playerAVG == "-": playerAVG = 0
                    if playerOPS == "-": playerOPS = 0
                    if playerHR == "-": playerHR = 0

                    # if playerSB == "-": playerSB = 0
                    # if playerRBI == "-": playerRBI = 0
                    # if playerR == "-": playerR = 0

                    if playerBB == "-": playerBB = 0
                    if playerIBB == "-": playerIBB = 0
                    if playerSF == "-": playerSF = 0
                    if playerHBP == "-": playerHBP = 0
                    if player1B == "-": player1B = 0
                    if player2B == "-": player2B = 0
                    if player3B == "-": player3B = 0
                    if playerSO == "-": playerSO = 0
                    if playerH == "-": playerH = 0

                    # Set playerWar if type is season, otherwise set to 0 since it is not available
                    try:
                        playerWAR = batterStats[j]['WAR']
                    except:
                        playerWAR = 0

                    if playerWAR == "-": playerWAR = 0

                    # Gets the player's weighted on base average if available using league constants from FanGraphs
                    try:
                        wOBA = ((League.wBB * float(playerBB)) + (League.wHBP * float(playerHBP)) + (League.w1B * float(player1B)) + (
                                    League.w2B * float(player2B)) + (
                                        League.w3B * float(player3B)) + (League.wHR * float(playerHR))) / (
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
                        wRC = (((float(wOBA) - League.obaW) / League.wOBAScale) + League.rPAW) * float(playerPA)
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
                        wRAA = ((float(wOBA) - float(League.obaW)) / float(League.wOBAScale)) * playerPA
                        playerParkFactor = League.ballParkDict[playerTeam] / 100

                        if playerTeam in League.nlTeamList:
                            wRCP = ((((float(wRAA) / float(playerPA)) + float(League.rPAW)) + (
                                        float(League.rPAW) - (float(playerParkFactor) * float(League.rPAW)))) / (float(League.nlWRC) / float(League.nlPA))) * 100
                        else:
                            wRCP = ((((float(wRAA) / float(playerPA)) + float(League.rPAW)) + (
                                        float(League.rPAW) - (float(playerParkFactor) * float(League.rPAW)))) / (float(League.alWRC) / float(League.alPA))) * 100
                        wRCP = "{:.3f}".format(wRCP)
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

                    # If time is season, add WAR to dict, otherwise dont
                    if time == "season":
                        playerDict = {
                playerName: [playerPA, float(bb), float(k), float(BABIP), float(playerAVG), float(playerOPS), float(wOBA),
                             float(wRC), float(playerWAR), float(wRCP), float(wRCPA)]}
                    else:
                        playerDict = {
                            playerName: [playerPA, float(bb), float(k), float(BABIP), float(playerAVG),
                                         float(playerOPS), float(wOBA),
                                         float(wRC), float(wRCP), float(wRCPA)]}

                    # Add the player to their respective dictionary
                    if status == 1:
                        takenBatterDict.update(playerDict)
                    elif status == 2:
                        faBatterDict.update(playerDict)
                    elif status == 3:
                        teamBatterDict.update(playerDict)

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

    @staticmethod
    def get_batter(time, player_id):
        """
        Function to query a batter giving the option for stat desired time range
        :param time: str - "season" || "lastmonth" || "lastweek"
        :param player_id: str - Id of the player to be analyzed
        :return: dict of desired batters based on the given status
        """
        # Get a list of batter stats given a player id and the desired time range
        batterStats = League.lg.player_stats(player_id, req_type=time)
        # Get a list of all details for a batter, primarily used for their team to get their ballpark factor
        pD = League.lg.player_details(int(player_id))

        # Read in leagueConstants as a data frame
        df = pd.read_csv("leagueConstants.csv")
        # Get the 'Season', 'Last Month', and 'Last Week' columns of the data frame
        season = df.Season
        lastmonth = df['Last Month']
        lastweek = df['Last Week']

        # Get the season weights
        League.obaW = season.loc[0]
        League.wOBAScale = season.loc[1]
        League.wBB = season.loc[2]
        League.wHBP = season.loc[3]
        League.w1B = season.loc[4]
        League.w2B = season.loc[5]
        League.w3B = season.loc[6]
        League.wHR = season.loc[7]
        League.rPAW = season.loc[8]

        # Set the AL and NL PA/WRC stats based on the time period
        if time == "season":
            League.alPA = season.loc[9]
            League.alWRC = season.loc[10]
            League.nlPA = season.loc[11]
            League.nlWRC = season.loc[12]
        elif time == "lastmonth":
            League.alPA = lastmonth.loc[9]
            League.alWRC = lastmonth.loc[10]
            League.nlPA = lastmonth.loc[11]
            League.nlWRC = lastmonth.loc[12]
        else:
            League.alPA = lastweek.loc[9]
            League.alWRC = lastweek.loc[10]
            League.nlPA = lastweek.loc[11]
            League.nlWRC = lastweek.loc[12]

        playerName = batterStats[0]['name']

        # Get the players team from our pD object
        playerTeam = pD[0]['editorial_team_full_name']

        playerAB = batterStats[0]['AB']  # Number of player at-bats
        playerAVG = batterStats[0]['AVG']  # Player's batting average
        playerOPS = batterStats[0]['OPS']  # Player's OBP + Slugging
        playerHR = batterStats[0]['HR']  # Number of home runs hit

        # playerRBI = batterStats[0]['RBI']  # Number of runs batted in
        # playerR = batterStats[0]['R']  # Number of runs scored
        # playerSB = batterStats[0]['SB']  # Number of stolen bases

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

        # if playerSB == "-": playerSB = 0
        # if playerRBI == "-": playerRBI = 0
        # if playerR == "-": playerR = 0

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

        # Set playerWar if type is season, otherwise set to 0 since it is not available
        try:
            playerWAR = batterStats[0]['WAR']
        except:
            playerWAR = 0

        if playerWAR == "-": playerWAR = 0

        # Gets the player's weighted on base average if available using league constants from FanGraphs
        try:
            wOBA = ((League.wBB * float(playerBB)) + (League.wHBP * float(playerHBP)) + (
                        League.w1B * float(player1B)) + (
                            League.w2B * float(player2B)) + (
                            League.w3B * float(player3B)) + (League.wHR * float(playerHR))) / (
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
            wRC = (((float(wOBA) - League.obaW) / League.wOBAScale) + League.rPAW) * float(playerPA)
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
            wRAA = ((float(wOBA) - float(League.obaW)) / float(League.wOBAScale)) * playerPA
            playerParkFactor = League.ballParkDict[playerTeam] / 100

            if playerTeam in League.nlTeamList:
                wRCP = ((((float(wRAA) / float(playerPA)) + float(League.rPAW)) + (
                        float(League.rPAW) - (float(playerParkFactor) * float(League.rPAW)))) / (
                                    float(League.nlWRC) / float(League.nlPA))) * 100
            else:
                wRCP = ((((float(wRAA) / float(playerPA)) + float(League.rPAW)) + (
                        float(League.rPAW) - (float(playerParkFactor) * float(League.rPAW)))) / (
                                    float(League.alWRC) / float(League.alPA))) * 100
                wRCP = "{:.3f}".format(wRCP)
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

        # If time is season, add WAR to dict, otherwise dont
        if time == "season":
            return {
                playerName: [playerPA, float(bb), float(k), float(BABIP), float(playerAVG), float(playerOPS), float(wOBA),
                             float(wRC), float(playerWAR), float(wRCP), float(wRCPA)]}
        else:
            return {
                playerName: [playerPA, float(bb), float(k), float(BABIP), float(playerAVG), float(playerOPS),
                             float(wOBA),
                             float(wRC), float(wRCP), float(wRCPA)]}


    @staticmethod
    def get_pitcher(time, player_id):
        """
        Function to query a pitcher given an id, with the option for stat desired time range
        :param time: str - "season" || "lastmonth" || "lastweek"
        :param player_id: str - Id of the player to be analyzed
        :return: desired pitcher's stats in the form of a dict
        """
        # Get a list of pitcher stats given player's id and the desired time range
        pitcherStats = League.lg.player_stats(player_id, req_type=time)

        playerName = pitcherStats[0]['name']

        playerGames = pitcherStats[0]['G']
        playerIP = pitcherStats[0]['IP']

        playerBF = pitcherStats[0]['BF']  # Number of batters faced
        playerBB = pitcherStats[0]['BB']  # Number of batters walked
        playerKP = pitcherStats[0]['K']  # Number of strikeouts

        playerHR = pitcherStats[0]['HR']  # Number of home runs allowed
        playerHBP = pitcherStats[0]['HBP']  # Number of batters hit with a pitch
        playerERA = pitcherStats[0]['ERA']  # Player's ERA
        playerWHIP = pitcherStats[0]['WHIP']  # Player's WHIP
        playerWin = pitcherStats[0]['W']      # Number of wins
        playerLoss = pitcherStats[0]['L']
        playerSV = pitcherStats[0]['SV']

        try:
            playerWAR = pitcherStats[0]['WAR']
        except:
            playerWAR = 0

        # Set every stat that is not available to 0.0
        if playerGames == "-":
            playerGames = 0
        if playerBF == "-":
            playerBF = 0
        if playerBB == "-":
            playerBB = 0
        if playerKP == "-":
            playerKP = 0

        if playerHR == "-":
            playerHR = 0
        if playerHBP == "-":
            playerHBP = 0
        if playerIP == "-":
            playerIP = 0
        if playerWAR == "-":
            playerWAR = 0
        if playerERA == "-":
            playerERA = 0
        if playerWHIP == "-":
            playerWHIP = 0
        if playerWin == "-":
            playerWin = 0
        if playerLoss == "-":
            playerLoss = 0
        if playerSV == "-":
            playerSV = 0

        # Set strikeouts before it is modified for K%
        strikeouts = playerKP

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
        bb = "{:.3f}".format(bb)
        kP = "{:.3f}".format(kP)

        # Calculate the FIP score if possible
        try:
            FIP = (13 * float(playerHR) + 3 * (float(playerBB) + float(playerHBP)) - 2 * float(strikeouts)) / float(
                playerIP)
            # Constant is the league average FPI score for 2021
            FIP = float(FIP) + float(League.FIP_Constant)
        except:
            FIP = 0

        FIP = "{:.3f}".format(FIP)

        # If time is season, add WAR to dict, otherwise dont
        if time == "season":
            return {
                playerName: [float(player_id), float(playerGames), float(playerIP), float(playerBF), float(bb), float(kP),
                             float(FIP), float(playerERA), float(playerWHIP), float(playerWAR), float(strikeouts),
                             float(playerHR), float(playerWin), float(playerLoss), float(playerSV)]}
        else:
            return {
                playerName: [float(player_id), float(playerGames), float(playerIP), float(playerBF), float(bb), float(kP),
                             float(FIP), float(playerERA), float(playerWHIP), float(strikeouts),
                             float(playerHR), float(playerWin), float(playerLoss), float(playerSV)]}


    @staticmethod
    def get_pitchers(time, status, qualified):
        """
        Function to query all pitchers giving the option for stat desired time range and what pitchers to include
        :param time: str - "season" || "lastmonth" || "lastweek"
        :param status: int - 0 == all pitchers, 1 == rostered pitchers, 2 == free agent pitchers, 3 == pitchers currently on your team
        :param qualified: bool - Whether or not to include only 'qualified' pitchers
        based on the time period selected
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
            for i in League.lg.taken_players():
                if i["position_type"] == "P":
                    takenPID.append(i["player_id"])
            for i in League.lg.free_agents('P'):
                    faPID.append(i["player_id"])
            for i in League.tm.roster(League.lg.current_week()):
                if i["position_type"] == "P":
                    teamPID.append(i["player_id"])
            allPID.append(takenPID)
            allPID.append(faPID)
            allPID.append(teamPID)
        # Add every taken pitcher to allPID
        elif status == 1:
            for i in League.lg.taken_players():
                if i["position_type"] == "P":
                    takenPID.append(i["player_id"])
            allPID.append(takenPID)
        # Add every FA pitcher to allPID
        elif status == 2:
            for i in League.lg.free_agents('P'):
                faPID.append(i["player_id"])
            allPID.append(faPID)
        # Add every pitcher on your team to allPID
        else:
            for i in League.tm.roster(League.lg.current_week()):
                if i["position_type"] == "P":
                    teamPID.append(i["player_id"])
            allPID.append(teamPID)

        # For every different list within allPID (up to 3: taken, fa, roster)
        for i in range(0, len(allPID)):
            # Get a list of pitcher stats given a list of player ids and the desired time range
            pitcherStats = League.lg.player_stats(allPID[i], req_type=time)

            for j in range(0, len(pitcherStats)):
                playerName = pitcherStats[j]['name']
                playerID = pitcherStats[j]['player_id']
                playerGames = pitcherStats[j]['G']
                playerIP = pitcherStats[j]['IP']
                playerBF = pitcherStats[j]['BF']  # Number of batters faced
                if playerBF == "-":
                    playerBF = 0
                if qualified:
                    if time == "season":
                        bfQualifier = 50
                    elif time == "lastmonth":
                        bfQualifier = 25
                    else:
                        bfQualifier = 10
                else:
                    bfQualifier = 0
                if float(int(playerBF)) > bfQualifier:
                    playerBB = pitcherStats[j]['BB']  # Number of batters walked
                    playerKP = pitcherStats[j]['K']  # Number of strikeouts

                    playerHR = pitcherStats[j]['HR']  # Number of home runs allowed
                    playerHBP = pitcherStats[j]['HBP']  # Number of batters hit with a pitch
                    playerERA = pitcherStats[j]['ERA']  # Player's ERA
                    playerWHIP = pitcherStats[j]['WHIP']  # Player's WHIP

                    playerWin = pitcherStats[j]['W']  # Number of wins
                    playerLoss = pitcherStats[j]['L']
                    playerSV = pitcherStats[j]['SV']

                    try:
                        playerWAR = pitcherStats[j]['WAR']
                    except:
                        playerWAR = 0

                    # Set every stat that is not available to 0.0
                    if playerBB == "-":
                        playerBB = 0
                    if playerKP == "-":
                        playerKP = 0

                    if playerHR == "-":
                        playerHR = 0
                    if playerHBP == "-":
                        playerHBP = 0
                    if playerIP == "-":
                        playerIP = 0
                    if playerWAR == "-":
                        playerWAR = 0
                    if playerERA == "-":
                        playerERA = 0
                    if playerWHIP == "-":
                        playerWHIP = 0
                    if playerGames == "-":
                        playerGames = 0
                    if playerWin == "-":
                        playerWin = 0
                    if playerLoss == "-":
                        playerLoss = 0
                    if playerSV == "-":
                        playerSV = 0

                    # Set strikeouts before it is modified for K%
                    strikeouts = playerKP

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
                    bb = "{:.3f}".format(bb)
                    kP = "{:.3f}".format(kP)

                    # Calculate the FIP score if possible
                    try:
                        FIP = (13 * float(playerHR) + 3 * (float(playerBB) + float(playerHBP)) - 2 * float(strikeouts)) / float(playerIP)
                        # Constant is the league average FPI score for 2021
                        FIP = float(FIP) + float(League.FIP_Constant)
                    except:
                        FIP = 0
                    FIP = "{:.3f}".format(FIP)

                    # If time is season, add WAR to dict, otherwise dont
                    if time == "season":
                        playerDict = {playerName: [playerID, playerGames, playerIP, playerBF, bb, kP, FIP, playerERA, playerWHIP,
                        playerWAR, strikeouts, playerHR, playerWin, playerLoss, playerSV]}
                    else:
                        playerDict = {playerName: [playerID, playerGames, playerIP, playerBF, bb, kP, FIP, playerERA, playerWHIP,
                        strikeouts, playerHR, playerWin, playerLoss, playerSV]}

                    # Add the player to their respective dictionary
                    if status == 1:
                        takenPlayerPDict.update(playerDict)
                    elif status == 2:
                        fAPitcherDict.update(playerDict)
                    elif status == 3:
                        teamPitcherDict.update(playerDict)

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


    @staticmethod
    def get_all_players(time, qualified):
        """
        Displays every single player in the yahoo league based on the time period
        and determines whether players need to meet certain qualifications to be considered
        :param time: str - "season" || "lastmonth" || "lastweek"
        :param qualified: bool - Whether or not to include only 'qualified' players based on the time
        period selected
        :return:
        """
        teamPitchers = League.get_pitchers(time, 3, qualified)
        teamBatters = League.get_batters(time, 3, qualified)

        print("All pitchers currently on your team:")
        League.print_pitchers(teamPitchers, False)

        print("All batters currently on your team:")
        League.print_batters(teamBatters, True)

        takenPitchers = League.get_pitchers(time, 1, qualified)
        takenBatters = League.get_batters(time, 1, qualified)

        print("All pitchers currently on teams:")
        League.print_pitchers(takenPitchers, False)

        print("All batters currently on teams:")
        League.print_batters(takenBatters, True)

        faPitchers = League.get_pitchers(time, 2, qualified)
        faBatters = League.get_batters(time, 2, qualified)

        print("All free-agent pitchers")
        League.print_pitchers(faPitchers, False)

        print("All free-agent batters")
        League.print_batters(faBatters, True)

    @staticmethod
    def pitcher_career_stats(player_name):
        """
        Return's a pitcher's career statistics given a name
        :param player_name: str - Name of player to be analyzed
        :return:
        """
        playerID = statsapi.lookup_player(player_name)[0]['id']

        playerCareer = statsapi.player_stat_data(playerID, 'pitching', 'career')

        playerID = playerCareer['id']
        playerCareer = playerCareer['stats'][0]['stats']
        playerGames = playerCareer['gamesPlayed']
        playerIP = playerCareer['inningsPitched']

        playerBF = playerCareer['atBats']  # Number of batters faced
        playerBB = playerCareer['baseOnBalls']  # Number of batters walked
        playerKP = playerCareer['strikeOuts']  # Number of strikeouts

        playerHR = playerCareer['homeRuns']  # Number of home runs allowed
        playerHBP = playerCareer['hitByPitch']  # Number of batters hit with a pitch
        playerERA = playerCareer['era']  # Player's ERA
        playerWHIP = playerCareer['whip']  # Player's WHIP
        playerWin = playerCareer['wins']
        playerLoss = playerCareer['losses']
        playerSV = playerCareer['saves']

        if playerGames == "-":
            playerGames = 0
        if playerBF == "-":
            playerBF = 0
        if playerBB == "-":
            playerBB = 0
        if playerKP == "-":
            playerKP = 0

        if playerHR == "-":
            playerHR = 0
        if playerHBP == "-":
            playerHBP = 0
        if playerIP == "-":
            playerIP = 0
        if playerERA == "-":
            playerERA = 0
        if playerWHIP == "-":
            playerWHIP = 0

        # Set strikeouts before it is modified for K%
        strikeouts = playerKP

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
        bb = "{:.3f}".format(bb)
        kP = "{:.3f}".format(kP)

        # Calculate the FIP score if possible
        try:
            FIP = (13 * float(playerHR) + 3 * (float(playerBB) + float(playerHBP)) - 2 * float(strikeouts)) / float(
                playerIP)
            # Constant is the league average FPI score for 2021
            FIP = float(FIP) + float(League.FIP_Constant)
        except:
            FIP = 0

        FIP = "{:.3f}".format(FIP)

        # Return the desired pitcher
        return {
            player_name: [float(playerID), float(playerGames), float(playerIP), float(playerBF), float(bb), float(kP),
                         float(FIP), float(playerERA), float(playerWHIP), float(strikeouts),
                         float(playerHR), float(playerWin), float(playerLoss), float(playerSV)]}

    @staticmethod
    def batter_career_stats(player_name):
        """
        Return's a batter's career statistics given a name
        :param player_name: str - Name of player to be analyzed
        :return:
        """
        playerID = statsapi.lookup_player(player_name)[0]['id']
        playerTeam = statsapi.lookup_player(player_name)[0]['currentTeam']['id']
        playerTeam = statsapi.get('team', {'teamId': playerTeam})['teams'][0]['name']

        playerCareer = statsapi.player_stat_data(playerID, 'hitting', 'career')
        playerCareer = playerCareer['stats'][0]['stats']

        playerAB = playerCareer['atBats']  # Number of player at-bats
        playerAVG = playerCareer['avg']  # Player's batting average
        playerOPS = playerCareer['ops']  # Player's OBP + Slugging
        playerHR = playerCareer['homeRuns']  # Number of home runs hit

        playerBB = playerCareer['baseOnBalls']  # Number of walks
        playerIBB = playerCareer['intentionalWalks']  # Number of intentional walks
        playerSF = playerCareer['sacFlies']  # Number of sacrifice flies
        playerHBP = playerCareer['hitByPitch']  # Number of times hit by a pitch

        player2B = playerCareer['doubles']  # Number of doubles
        player3B = playerCareer['triples']  # Number of triples
        playerPA = playerCareer['plateAppearances']  # Number of plate appearances
        playerSO = playerCareer['strikeOuts']  # Number of strikeouts
        playerH = playerCareer['hits']  # Number of hits

        player1B = playerH - playerHR - player2B - player3B

        # Set every stat that is not available to 0.0
        if playerAB == "-": playerAB = 0
        if playerAVG == "-": playerAVG = 0
        if playerOPS == "-": playerOPS = 0
        if playerHR == "-": playerHR = 0

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

        # Gets the player's weighted on base average if available using league constants from FanGraphs
        try:
            wOBA = ((League.wBB * float(playerBB)) + (League.wHBP * float(playerHBP)) + (
                        League.w1B * float(player1B)) + (
                            League.w2B * float(player2B)) + (
                            League.w3B * float(player3B)) + (League.wHR * float(playerHR))) / (
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
            wRAA = ((float(wOBA) - float(League.obaW)) / float(League.wOBAScale)) * playerPA
            playerParkFactor = League.ballParkDict[playerTeam] / 100

            if playerTeam in League.nlTeamList:
                wRCP = ((((float(wRAA) / float(playerPA)) + float(League.rPAW)) + (
                        float(League.rPAW) - (float(playerParkFactor) * float(League.rPAW)))) / (
                                    float(League.nlWRC) / float(League.nlPA))) * 100
            else:
                wRCP = ((((float(wRAA) / float(playerPA)) + float(League.rPAW)) + (
                        float(League.rPAW) - (float(playerParkFactor) * float(League.rPAW)))) / (
                                    float(League.alWRC) / float(League.alPA))) * 100
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
            player_name: [playerPA, float(bb), float(k), float(BABIP), float(playerAVG), float(playerOPS), float(wOBA),
                         float(wRC), float(wRCP), float(wRCPA)]}

    @staticmethod
    def outlier(player_name, status):
        """
        Displays whether a player is currently over or under-achieving
        comparing their current season statistics with their career statistics
        :param player_name: str - Name of player to be analyzed
        :param status: int - 0 == batter, 1 == pitcher
        :return:
        """
        currentSeasonStats = League.get_player(player_name, "season")
        if status == 0:
            careerStats = League.batter_career_stats(player_name)
            League.print_batters(currentSeasonStats, reverse=True)
            League.print_batters(careerStats, reverse=True)

            currentWRCPA = list(currentSeasonStats.values())[0][-1]
            currentWOBA = list(currentSeasonStats.values())[0][6]
            currentWRCP = list(currentSeasonStats.values())[0][9]

            careerWRCPA = list(careerStats.values())[0][-1]
            careerWOBA = list(careerStats.values())[0][6]
            careerWRCP = list(careerStats.values())[0][8]

            currTot = 0
            carTot = 0

            if currentWRCPA > careerWRCPA:
                currTot += 1
                diff = currentWRCPA - careerWRCPA
                diff = "{:.3f}".format(diff)
                print("Up " + str(diff) + " points in wRC/PA")
            else:
                carTot += 1
                diff = careerWRCPA - currentWRCPA
                diff = "{:.3f}".format(diff)
                print("Down " + str(diff) + " points in wRC/PA")
            if currentWOBA > careerWOBA:
                currTot += 1
                diff = currentWOBA - careerWOBA
                diff = "{:.3f}".format(diff)
                print("Up " + str(diff) + " points in wOBA")
            else:
                carTot += 1
                diff = careerWOBA - currentWOBA
                diff = "{:.3f}".format(diff)
                print("Down " + str(diff) + " points in wOBA")
            if currentWRCP > careerWRCP:
                currTot += 1
                diff = currentWRCP - careerWRCP
                diff = "{:.3f}".format(diff)
                print("Up " + str(diff) + " points in wRC+")
            else:
                carTot += 1
                diff = careerWRCP - currentWRCP
                diff = "{:.3f}".format(diff)
                print("Down " + str(diff) + " points in wRC+")
            if currTot > carTot:
                print("Currently overachieving based on the following categories:")
            else:
                print("Currently underacheiving based on the following categories:")
            print("wRC/PA, wOBA, wRC+")
        else:
            careerStats = League.pitcher_career_stats(player_name)
            League.print_pitchers(currentSeasonStats, reverse=True)
            League.print_pitchers(careerStats, reverse=True)

            currentFIP = list(currentSeasonStats.values())[0][6]
            currentERA = list(currentSeasonStats.values())[0][7]
            currentWHIP = list(currentSeasonStats.values())[0][8]
            currentKP = list(currentSeasonStats.values())[0][5]
            currentBP = list(currentSeasonStats.values())[0][4]

            careerFIP = list(careerStats.values())[0][6]
            careerERA = list(careerStats.values())[0][7]
            careerWHIP = list(careerStats.values())[0][8]
            careerKP = list(careerStats.values())[0][5]
            careerBP = list(careerStats.values())[0][4]

            currTot = 0
            carTot = 0

            if currentFIP < careerFIP:
                currTot += 1
                diff = careerFIP - currentFIP
                diff = "{:.3f}".format(diff)
                print("Up " + str(diff) + " points in FIP")
            else:
                carTot += 1
                diff = currentFIP - careerFIP
                diff = "{:.3f}".format(diff)
                print("Down " + str(diff) + " points in FIP")
            if currentERA < careerERA:
                currTot += 1
                diff = careerERA - currentERA
                diff = "{:.3f}".format(diff)
                print("Up " + str(diff) + " points in ERA")
            else:
                carTot += 1
                diff = currentERA - careerERA
                diff = "{:.3f}".format(diff)
                print("Down " + str(diff) + " points in ERA")
            if currentWHIP < careerWHIP:
                currTot += 1
                diff = careerWHIP - currentWHIP
                diff = "{:.3f}".format(diff)
                print("Up " + str(diff) + " points in WHIP")
            else:
                carTot += 1
                diff = currentWHIP - careerWHIP
                diff = "{:.3f}".format(diff)
                print("Down " + str(diff) + " points in WHIP")
            if currentKP > careerKP:
                currTot += 1
                diff = currentKP - careerKP
                diff = "{:.3f}".format(diff)
                print("Up " + str(diff) + " points in K%")
            else:
                carTot += 1
                diff = careerKP - currentKP
                diff = "{:.3f}".format(diff)
                print("Down " + str(diff) + " points in K%")
            if currentBP < careerBP:
                currTot += 1
                diff = careerBP - currentBP
                diff = "{:.3f}".format(diff)
                print("Up " + str(diff) + " points in BB%")
            else:
                carTot += 1
                diff = currentBP - careerBP
                diff = "{:.3f}".format(diff)
                print("Down " + str(diff) + " points in BB%")

            if currTot > carTot:
                print("Currently overachieving based on the following categories:")
            else:
                print("Currently underacheiving based on the following categories:")
            print("FIP, ERA, WHIP, K%, BB%")

    @staticmethod
    def whos_hot(time):
        """
        Displays the 10 best qualified free agent / taken pitchers and batters
        over the desired time period based on FIP and WRC+
        :param time: str - "season" || "lastmonth" || "lastweek"
        :return:
        """
        # Print top 10 pitcher free agents and taken players
        ttRP = dict(list(League.get_pitchers(time, 1, qualified=True).items()))
        hotPList = dict(sorted(ttRP.items(), key=lambda item: item[1][6])[0:10])
        print("\n" + "Top 10 Hottest Rostered Pitchers: ")
        League.print_pitchers(hotPList, reverse=False)

        ttFAP = dict(list(League.get_pitchers(time, 2, qualified=True).items()))
        hotPList2 = dict(sorted(ttFAP.items(), key=lambda item: item[1][6])[0:10])
        print("\n" + "Top 10 Hottest Free Agent Pitchers: ")
        League.print_pitchers(hotPList2, reverse=False)

        # Print top 10 batter free agents and taken players
        ttRB = dict(list(League.get_batters(time, 1, qualified=True).items()))
        hotBList = dict(sorted(ttRB.items(), key=lambda item: item[1][6], reverse=True)[0:10])
        print("\n" + "Top 10 Hottest Rostered Batters: ")
        League.print_batters(hotBList, reverse=True)

        ttFAB = dict(list(League.get_batters(time, 2, qualified=True).items()))
        hotBList2 = dict(sorted(ttFAB.items(), key=lambda item: item[1][6], reverse=True)[0:10])
        print("\n" + "Top 10 Hottest Free Agent Batters: ")
        League.print_batters(hotBList2, reverse=True)

    @staticmethod
    def whos_cold(time):
        """
        Displays the 10 worst qualified free agent / taken pitchers and batters
        over the desired time period based on FIP and WRC+
        :param time: str - "season" || "lastmonth" || "lastweek"
        :return:
        """
        # Print top 10 worst pitcher free agents and taken players
        ttRP = dict(list(League.get_pitchers(time, 1, qualified=True).items()))
        coldPList = dict(sorted(ttRP.items(), key=lambda item: item[1][6], reverse=True)[0:10])
        print("\n" + "Top 10 Coldest Rostered Pitchers: ")
        League.print_pitchers(coldPList, reverse=True)

        ttFAP = dict(list(League.get_pitchers(time, 2, qualified=True).items()))
        coldPList2 = dict(sorted(ttFAP.items(), key=lambda item: item[1][6], reverse=True)[0:10])
        print("\n" + "Top 10 Coldest Free Agent Pitchers: ")
        League.print_pitchers(coldPList2, reverse=True)

        # Print top 10 worst batter free agents and taken players
        ttRB = dict(list(League.get_batters(time, 1, qualified=True).items()))
        coldBList = dict(sorted(ttRB.items(), key=lambda item: item[1][6])[0:10])
        print("\n" + "Top 10 Coldest Rostered Batters: ")
        League.print_batters(coldBList, reverse=False)

        ttFAB = dict(list(League.get_batters(time, 2, qualified=True).items()))
        coldBList2 = dict(sorted(ttFAB.items(), key=lambda item: item[1][6])[0:10])
        print("\n" + "Top 10 Coldest Free Agent Batters: ")
        League.print_batters(coldBList2, reverse=False)
