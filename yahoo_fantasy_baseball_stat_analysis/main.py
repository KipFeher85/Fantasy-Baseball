import yaml
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
import pandas as pd
from datetime import date
import statsapi
from dateutil.relativedelta import relativedelta


class League:
    def __init__(self, year):
        
        # Obtain Yahoo OAuth2 access token from the file given
        self.oauth = OAuth2(None, None, from_file='OAuth2.json')

        # Create a Yahoo Fantasy MLB Game object using the access token
        self.gm = yfa.Game(self.oauth, 'mlb')

        # Get the league id desired
        self.leagueID = self.gm.league_ids(year=year)[0]
    
        # Create a league object given the first id of the user's league id's for the season
        self.lg = self.gm.to_league(self.leagueID)
    
        # Create a team object given the team's key
        self.tm = self.lg.to_team(team_key=self.lg.team_key())

        # Set the desired year
        self.yr = year
    
        # Create dict to hold ballpark factors, lists to hold NL and AL team names
        self.ballParkDict = {}
        self.alTeamList = []
        self.nlTeamList = []
    
        self.obaW = 0
        self.wOBAScale = 0
        self.wBB = 0
        self.wHBP = 0
        self.w1B = 0
        self.w2B = 0
        self.w3B = 0
        self.wHR = 0
        self.rPAW = 0  # wRAA weight
    
        self.alPA = 0
        self.alWRC = 0
        self.nlPA = 0
        self.nlWRC = 0
    
        self.FIP_Constant = 0

        self.__configs = yaml.load(open("configs.yaml"), Loader=yaml.FullLoader)

    def update_ballpark_constants(self):
        """
        THIS FUNCTION ONLY NEEDS TO BE CALLED ONCE PER SEASON
        This function allows the user to not exceed the rate-limit for any api

        Gets the following ballpark factors for the season from fangraphs:
        - Basic, 1B, 2B, 3B, HR, SO, BB, GB, FB, LD, IFFB, FIP

        Writes this data to a json file 'ballParkFactors.json'
        :return:
        """
        # Get df of all the ballpark constants
        guts = pd.read_html(f"https://www.fangraphs.com/guts.aspx?type=pf&teamid=0&season={self.yr - 1}")[8]
        # Create a array to hold the ballpark constant dict
        team_dict = {
            "Teams": {}
        }
        for i in range(0, len(guts)):
            full_team_name = statsapi.lookup_team(guts.iloc[i][1], activeStatus="Y", season=self.yr)[0]["name"]
            team_dict["Teams"][full_team_name] = {
                "Basic": int(guts.iloc[i][2]),
                "1B": int(guts.iloc[i][5]),
                "2B": int(guts.iloc[i][6]),
                "3B": int(guts.iloc[i][7]),
                "HR": int(guts.iloc[i][8]),
                "SO": int(guts.iloc[i][9]),
                "BB": int(guts.iloc[i][10]),
                "GB": int(guts.iloc[i][11]),
                "FB": int(guts.iloc[i][12]),
                "LD": int(guts.iloc[i][13]),
                "IFFB": int(guts.iloc[i][14]),
                "FIP": int(guts.iloc[i][15])
            }
        with open("ballParkFactors.json", "w") as outfile:
            json.dump(team_dict, outfile, indent=4)

    def update_league_constants(self):
        """
        THIS FUNCTION ONLY NEEDS TO BE CALLED ONCE PER DAY
        This function allows the user to not exceed the rate-limit for any api

        Gets the following weights for the season from fangraphs:
        - OBA, wOBA Scale, wBB, wHBP, w1B, w2B, w3B, wHR, wRAA weight
        Gets PA and WRC stats for both NL and AL over the following time periods:
        - Season, Last Month (From the current day), Last Week (From the current day)

        Writes this data to a json file 'leagueConstants.json'
        :return:
        """
        # Url for the fangraphs 'GUTS' page
        gutsURL = "https://www.fangraphs.com/guts.aspx?type=cn"
        # Turn the html page into a dataframe
        gutsDF = pd.read_html(gutsURL)[8].loc[0]

        # Set the League object's weights
        self.obaW = float(gutsDF[1])
        self.wOBAScale = float(gutsDF[2])
        self.wBB = float(gutsDF[3])
        self.wHBP = float(gutsDF[4])
        self.w1B = float(gutsDF[5])
        self.w2B = float(gutsDF[6])
        self.w3B = float(gutsDF[7])
        self.wHR = float(gutsDF[8])
        self.rPAW = float(gutsDF[11])  # wRAA weight
        self.FIP_Constant = float(gutsDF[13])

        # Create a list to hold the urls for NL and AL stats over different time periods
        alURList = []
        nlURList = []

        # Get today's date
        month = date.today().strftime("%m")
        day = date.today().strftime("%d")
        year = "20" + date.today().strftime("%y")

        # Set the url to get AL and NL league stats for the season
        alURL = f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=al&qual=0&type=1&season={year}&month=1000&season1={year}&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-{month}-{day}"
        nlURL = f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=nl&qual=0&type=1&season={year}&month=1000&season1={year}&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-{month}-{day}"
        alURList.append(alURL)
        nlURList.append(nlURL)

        # Get the date of previous month from current day
        last_month = date.today() - relativedelta(months=1)
        lMonth = last_month.strftime("%m")
        lDay = last_month.strftime("%d")
        lYear = "20" + last_month.strftime("%y")

        # Set the url to get AL and NL league stats for the last month
        alURList.append(f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=al&qual=0&type=1&season={year}&month=1000&season1={year}&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate={lYear}-{lMonth}-{lDay}&enddate={year}-{month}-{day}")
        nlURList.append(f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=nl&qual=0&type=1&season={year}&month=1000&season1={year}&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate={lYear}-{lMonth}-{lDay}&enddate={year}-{month}-{day}")

        # Get the date of previous week from current day
        last_week = date.today() - relativedelta(weeks=1)
        lMonth = last_week.strftime("%m")
        lDay = last_week.strftime("%d")
        lYear = "20" + last_week.strftime("%y")

        # Set the url to get AL and NL league stats for the last week
        alURList.append(f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=al&qual=0&type=1&season={year}&month=1000&season1={year}&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate={lYear}-{lMonth}-{lDay}&enddate={year}-{month}-{day}")
        nlURList.append(f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=nl&qual=0&type=1&season={year}&month=1000&season1={year}&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate={lYear}-{lMonth}-{lDay}&enddate={year}-{month}-{day}")

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
        json_dict = {
            "OBA Weight": self.obaW,
            'wOBA Scale': self.wOBAScale,
            'BB Weight': self.wBB,
            'HBP Weight': self.wHBP,
            '1B Weight': self.w1B,
            '2B Weight': self.w2B,
            '3B Weight': self.w3B,
            'HR Weight': self.wHR,
            'wRAA Weight': self.rPAW,
            'AL Plate Appearances': {
                "Season": int(alPAList[0]), 
                "Last Month": int(alPAList[1]), 
                "Last Week": int(alPAList[2])
            },
            'AL Weighted Runs Created': {
                "Season": int(alWRCList[0]), 
                "Last Month": int(alWRCList[1]), 
                "Last Week": int(alWRCList[2])
            },
            'NL Plate Appearances': {
                "Season": int(nlPAList[0]), 
                "Last Month": int(nlPAList[1]), 
                "Last Week": int(nlPAList[2])
            },
            'NL Weighted Runs Created': {
                "Season": int(nlWRCList[0]), 
                "Last Month": int(nlWRCList[1]), 
                "Last Week": int(nlWRCList[2])
            },
            'FIP Constant': self.FIP_Constant
        }
        with open("leagueConstants.json", "w") as outfile:
            json.dump(json_dict, outfile, indent=4)

    def starter(self):
        """
        Initializes the league object, needs to be always be called
        - Gets list of NL and AL teams in addition to each ball park factor
        - Grabs the season FIP constant from 'leagueConstants.json'
        :return:
        """

        # Open json file containing teams and ballpark factors as a file object
        with open('ballParkFactors.json') as f:
            # Create lists for each team and ballpark factors
            teamList = []
            bfList = []
            nlBFList = []
            alBFList = []
            # Create json object from file
            data = json.load(f)
            teams = list(data["Teams"].keys())
            # Add each team and ballpark factor to their respective lists
            for i in range(0, len(teams)):
                teamList.append(teams[i])
                basic = int(data["Teams"][teams[i]]["Basic"])
                bfList.append(basic)
                if i in range(0, 14):
                    alBFList.append(basic)
                else:
                    nlBFList.append(basic)
        # Add every team and their respective ballpark factor to the dict
        for i in range(0, len(teamList)):
            self.ballParkDict.update({teamList[i]: bfList[i]})
        # Add every AL team to a list
        for i in range(0, 14):
            self.alTeamList.append(teamList[i])
        # Add every NL team to a list
        for i in range(14, len(teamList)):
            self.nlTeamList.append(teamList[i])
        # Add a column to the dict for both the NL and AL avg ballpark factor
        self.ballParkDict.update({"NL Avg": sum(nlBFList) / len(nlBFList)})
        self.ballParkDict.update({"AL Avg": sum(alBFList) / len(alBFList)})
        # Set the league's FIP constant
        self.FIP_Constant = json.load(open("leagueConstants.json"))["FIP Constant"]

    def get_player(self, player_name, time):
        """
        Returns a player's stats over the specified time period given a name
        :param player_name: str
        :param time: str - "season" || "lastmonth" || "lastweek"
        :return: Dict
        """
        playerDict = {}
        try:
            # Grab the player's id and position
            playerId = self.lg.player_details(player_name)[0]['player_id']
            playerPos = self.lg.player_details(player_name)[0]['position_type']

            # If player is a batter
            if playerPos == 'B':
                # Get the player's stats as a dict
                playerDict = self.get_batter(time, playerId)
                # Print the desired batter
            elif playerPos == 'P':
                playerDict = self.get_pitcher(time, playerId)
            return playerDict
        except Exception as e:
            print("Player Details Error: ", e)
            # If player is not available display message
            return str(player_name) + "'s stats not available"

    def print_player(self, player_name, time):
        """
        Display's the desired player's stats over the desired time period
        :param player_name: str - Player name
        :param time: str - "season" || "lastmonth" || "lastweek"
        :return:
        """
        # If player is a batter
        playerDict = self.get_player(player_name, time)
        if playerDict != str(player_name) + "'s stats not available":
            playerPos = self.lg.player_details(player_name)[0]['position_type']
            if playerPos == 'B':
                # Print the desired batter
                self.print_batters(playerDict, reverse=True)
            elif playerPos == 'P':
                self.print_pitchers(playerDict, reverse=False)
        else:
            # If player is not available display message
            print(playerDict)

    def current_roster_stats(self, time):
        """
        Display roster and their advanced stats over the desired time period
        :param time: str - "season" || "lastmonth" || "lastweek"
        :return:
        """
        print("Your batters: ")
        # Get the dict of all batters currently on your team
        team_batters = self.get_batters(time, 3, False)
        # Print every batter and their advanced stats in currentBatters
        self.print_batters(team_batters, True)

        print("\n" + "Your pitchers: ")
        # Get the dict of all pitchers currently on your team
        team_pitchers = self.get_pitchers(time, 3, False)
        # Print every pitcher and their advanced stats in currentPitchers
        self.print_pitchers(team_pitchers, False)

    def current_roster_basic(self):
        """
        Display's a player's entire roster without their stats but player details (Player Id, Position, Eligible Postions, Status)
        :return:
        """
        hitterList = []
        pitcherList = []
        injuredList = []

        # Iterate through every player on the team within the current week
        for i in self.tm.roster(self.lg.current_week()):
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
        print("\n" + "IL, DTD, NA: ")
        for i in injuredList:
            print(i)

    def team_details(self):
        """
        Gives basic details for every team in the league including name, owner, owner legacy, logo info
        :return:
        """
        # Get dict of all teams in the league
        tms = self.lg.teams()
        for i in tms:
            print(list(tms[i].items()))

    def predict_team_day(self):
        """
        Function to help aid in the selection of players for the daily lineup
        Displays the probable pitchers for every game
        Probable pitcher's name, pregame note, and advanced stats from their past month are shown
        User's batter and pitcher advanced stats over the past week are displayed as well
        :return:
        """
        # Create a dictionary of all the games being played today
        today = statsapi.schedule(date.today())
        if(len(today)) > 0:
            game_list = []
            # For every game on the schedule
            for game in today:
                hN = game["home_pitcher_note"]
                if hN == "": hN = "Not Available"
                aN = game["away_pitcher_note"]
                if aN == "": aN = "Not Available"
                if game["home_probable_pitcher"] == "Shohei Ohtani":
                    h_id = "1000002"
                else:
                    h_id = self.lg.player_details(game["home_probable_pitcher"])[0]['player_id']
                if game["home_probable_pitcher"] == "Shohei Ohtani":
                    a_id = "1000002"
                else:
                    a_id = self.lg.player_details(game["away_probable_pitcher"])[0]['player_id']
                game_list.append({
                    "Home Name": game["home_name"],
                    "Away Name": game["away_name"],
                    "Home Pitcher": {
                        "Name": game["home_probable_pitcher"],
                        "ID": h_id,
                        "Stats": self.get_pitcher("lastmonth", h_id),
                        "Note": hN
                    },
                    "Away Pitcher": {
                        "Name": game["away_probable_pitcher"],
                        "ID": a_id,
                        "Stats": self.get_pitcher("lastmonth", a_id),
                        "Note": aN
                    }
                })
            for i in range(0, len(game_list)):
                print("\nGame " + str(i + 1) + ": " + str(game_list[i]["Away Name"]) + " at " + str(game_list[i]["Home Name"]))
                print("Pitcher Stats over the past month")
                try:
                    hPitcherName = game_list[i]['Home Pitcher']['Name']
                    hPitcher = game_list[i]["Home Pitcher"]["Stats"][hPitcherName]
                    hPitcherNote = game_list[i]["Home Pitcher"]["Note"]
                    print(f"HP: {hPitcherName} IP: {hPitcher['IP']} BF: {hPitcher['BF']} BB%: {hPitcher['BB']} K%: {hPitcher['SO%']} FIP: {hPitcher['FIP']} ERA: {hPitcher['ERA']} WHIP: {hPitcher['WHIP']} K: {hPitcher['K']} HR: {hPitcher['HR']}")
                    print(str(hPitcherName) + " Note: " + hPitcherNote)
                except Exception as e:
                    print("HP: There isnt a specified pitcher or the pitcher's information is unavailable")
                try:
                    aPitcherName = game_list[i]['Away Pitcher']['Name']
                    aPitcher = game_list[i]["Away Pitcher"]["Stats"][aPitcherName]
                    aPitcherNote = game_list[i]["Away Pitcher"]["Note"]
                    print(f"AP: {aPitcherName} IP: {aPitcher['IP']} BF: {aPitcher['BF']} BB%: {aPitcher['BB']} K%: {aPitcher['SO%']} FIP: {aPitcher['FIP']} ERA: {aPitcher['ERA']} WHIP: {aPitcher['WHIP']} K: {aPitcher['K']} HR: {aPitcher['HR']}")
                    print(str(aPitcherName) + " Note: " + aPitcherNote)
                except Exception as e:
                    print("AP: There isnt a specified pitcher or the pitcher's information is unavailable")
        else:
            print("There are no games today :/")

        print("\nTeam batter stats over the past week: ")
        # Create a dict containing the stats of all batters on team over the past week
        teamBatters = self.get_batters(time="lastweek", status=3, qualified=False)
        # Print every batter in teamBatters
        self.print_batters(teamBatters, reverse=True)

        print("\nTeam pitcher stats over the past week: ")
        # Create a dict containing the stats of all pitchers on team over the past week
        teamPitchers = self.get_pitchers(time="lastweek", status=3, qualified=False)
        # Print every batter in teamPitchers
        self.print_pitchers(teamPitchers, reverse=False)

    def print_batters(self, ed_dict, reverse):
        """
        Useful function to print a dict of batters that is ed, 'edDict'
        :param ed_dict: Dict - Contains a dictionary of batters that need printed
        :param reverse: bool - True: Desc, False: Asc
        :return:
        """
        sortedBList = sorted(ed_dict.items(), key=lambda item: item[1]["wRCP"], reverse=reverse)
        for i in sortedBList:
            if "WAR" in i[1]:
                print(f"Name: {i[0]} PA: {i[1]['PA']} wRC: {i[1]['wRC']} wRC/PA: {i[1]['wRCPA']} wOBA: {i[1]['wOBA']} BABIP: {i[1]['BABIP']} wRC+: {i[1]['wRCP']} WAR: {i[1]['WAR']}")
            else:
                print(f"Name: {i[0]} PA: {i[1]['PA']} wRC: {i[1]['wRC']} wRC/PA: {i[1]['wRCPA']} wOBA: {i[1]['wOBA']} BABIP: {i[1]['BABIP']} wRC+: {i[1]['wRCP']}")

    def print_pitchers(self, ed_dict, reverse):
        """
        Useful function to print a dict of pitchers that is ed, 'edDict'
        :param ed_dict: Dict - Contains a dictionary of pitchers that need printed
        :param reverse: bool - True: Desc, False: Asc
        :return:
        """
        sortedPList = sorted(ed_dict.items(), key=lambda item: item[1]["FIP"], reverse=reverse)
        # Created a sorted list of pitchers, based on their FIP in descending order
        for i in sortedPList:
            if "WAR" in i[1]:
                # If type equals 'season', print WAR. If it doesnt then dont include WAR since it cant be calculated
                print(f"Name: {i[0]} GS: {i[1]['GP']} IP: {i[1]['IP']} BF: {i[1]['BF']} BB%: {i[1]['BB']} K%: {i[1]['SO%']} FIP: {i[1]['FIP']} ERA: {i[1]['ERA']} WHIP: {i[1]['WHIP']} WAR: {i[1]['WAR']} W: {i[1]['W']} L: {i[1]['L']} SV: {i[1]['SV']}")
            else:
                print(f"Name: {i[0]} GS: {i[1]['GP']} IP: {i[1]['IP']} BF: {i[1]['BF']} BB%: {i[1]['BB']} K%: {i[1]['SO%']} FIP: {i[1]['FIP']} ERA: {i[1]['ERA']} WHIP: {i[1]['WHIP']} W: {i[1]['W']} L: {i[1]['L']} SV: {i[1]['SV']}")

    def get_batters(self, time, status, qualified):
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
            for i in self.lg.taken_players():
                if i["position_type"] == "B":
                    takenBID.append(i["player_id"])
            for i in self.lg.free_agents('B'):
                faBID.append(i["player_id"])
            for i in self.tm.roster(self.lg.current_week()):
                if i["position_type"] == "B":
                    teamBID.append(i["player_id"])
            allBID.append(takenBID)
            allBID.append(faBID)
            allBID.append(teamBID)
        # Add every taken batter to allBID
        elif status == 1:
            for i in self.lg.taken_players():
                if i["position_type"] == "B":
                    takenBID.append(i["player_id"])
            allBID.append(takenBID)
        # Add every FA batter to allBID
        elif status == 2:
            for i in self.lg.free_agents('B'):
                if i["position_type"] == "B":
                    faBID.append(i["player_id"])
            allBID.append(faBID)
        # Add every batter on your team to allBID
        else:
            for i in self.tm.roster(self.lg.current_week()):
                if i["position_type"] == "B":
                    teamBID.append(i["player_id"])
            allBID.append(teamBID)

        df = json.load(open("leagueConstants.json"))
        # Get the season weights
        self.obaW = df["OBA Weight"]
        self.wOBAScale = df["wOBA Scale"]
        self.wBB = df["BB Weight"]
        self.wHBP = df["HBP Weight"]
        self.w1B = df["1B Weight"]
        self.w2B = df["2B Weight"]
        self.w3B = df["3B Weight"]
        self.wHR = df["HR Weight"]
        self.rPAW = df["wRAA Weight"]

        # Set the AL and NL PA/WRC stats based on the time period
        alPA = df["AL Plate Appearances"]
        nlPA = df["NL Plate Appearances"]
        alWRC = df["AL Weighted Runs Created"]
        nlWRC = df["NL Weighted Runs Created"]
        if time == "season":
            self.alPA = alPA["Season"]
            self.alWRC = alWRC["Season"]
            self.nlPA = nlPA["Season"]
            self.nlWRC = nlWRC["Season"]
        elif time == "lastmonth":
            self.alPA = alPA["Last Month"]
            self.alWRC = alWRC["Last Month"]
            self.nlPA = nlPA["Last Month"]
            self.nlWRC = nlWRC["Last Month"]
        else:
            self.alPA = alPA["Last Week"]
            self.alWRC = alWRC["Last Week"]
            self.nlPA = nlPA["Last Week"]
            self.nlWRC = nlWRC["Last Week"]
        # Determine whether or not the qualifier is used
        if qualified:
            if time == "season":
                paQualifier = self.__configs["plate_appearances_season"]
            elif time == "lastmonth":
                paQualifier = self.__configs["plate_appearances_month"]
            else:
                paQualifier = self.__configs["plate_appearances_week"]
        else:
            paQualifier = 0

        # For every different list within allBID (up to 3: taken, fa, roster)
        for i in range(0, len(allBID)):
            # Get a list of batter stats given a list of player ids and the desired time range
            batterStats = self.lg.player_stats(allBID[i], req_type=time)
            # Get a list of all details for a batter, primarily used for their team to get their ballpark factor
            pD = self.lg.player_details(allBID[i])
            # For every batter in our current list
            for j in range(0, len(batterStats)):
                # Set every stat that is not available to 0.0
                batter = batterStats[j]
                batter_keys = list(batter.keys())
                for k in batter_keys:
                    if batter[k] == "-": batter[k] = 0
                playerName = batter['name']
                # Get the players team from our pD object
                playerTeam = pD[j]['editorial_team_full_name']
                playerAB = batter['AB']  # Number of player at-bats
                playerPA = batter['PA']  # Number of plate appearances
                if float(int(playerPA)) >= paQualifier:
                    playerAVG = batter['AVG']  # Player's batting average
                    playerOPS = batter['OPS']  # Player's OBP + Slugging
                    playerHR = batter['HR']  # Number of home runs hit
                    playerBB = batter['BB']  # Number of walks
                    playerIBB = batter['IBB']  # Number of intentional walks
                    playerSF = batter['SF']  # Number of sacrifice flies
                    playerHBP = batter['HBP']  # Number of times hit by a pitch
                    player1B = batter['1B']  # Number of singles
                    player2B = batter['2B']  # Number of doubles
                    player3B = batter['3B']  # Number of triples
                    playerSO = batter['SO']  # Number of strikeouts
                    playerH = batter['H']  # Number of hits
                    # Set playerWar if type is season, otherwise set to 0 since it is not available
                    try:
                        playerWAR = batter['WAR']
                    except Exception as e:
                        # print("Failed to get the player's WAR rating. Only available for a players season stats. Not last month or week")
                        playerWAR = 0
                    # Gets the player's weighted on base average if available using league constants from FanGraphs
                    try:
                        wOBA = ((self.wBB * playerBB) + (self.wHBP * playerHBP) + (self.w1B * player1B) + (
                                    self.w2B * player2B) + (self.w3B * player3B) + (self.wHR * playerHR)) / (
                                           playerAB + playerBB - playerIBB + playerSF + playerHBP)
                        wOBA = float("{:.3f}".format(wOBA))
                    except Exception as e:
                        # print("wOBA Error: ", e)
                        wOBA = 0
                    # Get the player's batting average on balls in play
                    try:
                        BABIP = (playerH - playerHR) / (playerAB - playerHR - playerSO + playerSF)
                        BABIP = float("{:.3f}".format(BABIP))
                    except Exception as e:
                        # print("BABIP Error: ", e)
                        BABIP = 0
                    # Gets the player's number of weighted runs scored
                    try:
                        wRC = (((wOBA - self.obaW) / self.wOBAScale) + self.rPAW) * playerPA
                        wRC = float("{:.3f}".format(wRC))
                    except Exception as e:
                        # print("wRC Error: ", e)
                        wRC = 0
                    # Gets the player's number of weighted runs created per plate appearance
                    try:
                        wRCPA = float(wRC) / playerPA
                        wRCPA = float("{:.3f}".format(wRCPA))
                    except Exception as e:
                        # print("wRC/PA Error: ", e)
                        wRCPA = 0
                    # Gets the player's weighted runs above average which gives us their weighted runs created plus which incorporates ballpark factors
                    try:
                        # wRAA = ((wOBA – league wOBA) / wOBA scale) × PA
                        wRAA = ((wOBA - self.obaW) / self.wOBAScale) * playerPA
                        playerParkFactor = self.ballParkDict[playerTeam] / 100
                        # wRC+ = (((wRAA/PA + League R/PA) + (League R/PA – Park Factor* League R/PA))/ (AL or NL wRC/PA excluding pitchers))*100
                        if playerTeam in self.nlTeamList:
                            wRCP = ((((wRAA / playerPA) + self.rPAW) + (self.rPAW - (playerParkFactor * self.rPAW))) / (
                                        self.nlWRC / self.nlPA)) * 100
                        else:
                            wRCP = ((((wRAA / playerPA) + self.rPAW) + (self.rPAW - (playerParkFactor * self.rPAW))) / (
                                        self.alWRC / self.alPA)) * 100
                        wRCP = float("{:.3f}".format(wRCP))
                    except Exception as e:
                        # print("wRC+ Error: ", e)
                        wRCP = 0
                    # Get the players walk and strikeout percentages
                    try:
                        bb = (playerBB / playerAB) * 100
                        bb = float("{:.3f}".format(bb))
                    except Exception as e:
                        # print("BB Error: ", e)
                        bb = 0
                    try:
                        k = (playerSO / playerAB) * 100
                        k = float("{:.3f}".format(k))
                    except Exception as e:
                        # print("K Error: ", e)
                        k = 0
                    player_dict = {
                        playerName: {
                            "PA": playerPA,
                            "BB": bb,
                            "K": k,
                            "BABIP": BABIP,
                            "AVG": playerAVG,
                            "OPS": playerOPS,
                            "wOBA": wOBA,
                            "wRC": wRC,
                            "wRCPA": wRCPA,
                            "wRCP": wRCP
                        }
                    }
                    # If time is season, add WAR to dict, otherwise dont
                    if time == "season":
                        player_dict[playerName]["WAR"] = playerWAR
                    # Add the player to their respective dictionary
                    if status == 1:
                        takenBatterDict.update(player_dict)
                    elif status == 2:
                        faBatterDict.update(player_dict)
                    elif status == 3:
                        teamBatterDict.update(player_dict)
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

    def get_batter(self, time, player_id):
        """
        Function to query a batter giving the option for stat desired time range
        :param time: str - "season" || "lastmonth" || "lastweek"
        :param player_id: str - Id of the player to be analyzed
        :return: dict of desired batters based on the given status
        """
        df = json.load(open("leagueConstants.json"))
        # Get the season weights
        self.obaW = df["OBA Weight"]
        self.wOBAScale = df["wOBA Scale"]
        self.wBB = df["BB Weight"]
        self.wHBP = df["HBP Weight"]
        self.w1B = df["1B Weight"]
        self.w2B = df["2B Weight"]
        self.w3B = df["3B Weight"]
        self.wHR = df["HR Weight"]
        self.rPAW = df["wRAA Weight"]

        # Set the AL and NL PA/WRC stats based on the time period
        alPA = df["AL Plate Appearances"]
        nlPA = df["NL Plate Appearances"]
        alWRC = df["AL Weighted Runs Created"]
        nlWRC = df["NL Weighted Runs Created"]
        if time == "season":
            self.alPA = alPA["Season"]
            self.alWRC = alWRC["Season"]
            self.nlPA = nlPA["Season"]
            self.nlWRC = nlWRC["Season"]
        elif time == "lastmonth":
            self.alPA = alPA["Last Month"]
            self.alWRC = alWRC["Last Month"]
            self.nlPA = nlPA["Last Month"]
            self.nlWRC = nlWRC["Last Month"]
        else:
            self.alPA = alPA["Last Week"]
            self.alWRC = alWRC["Last Week"]
            self.nlPA = nlPA["Last Week"]
            self.nlWRC = nlWRC["Last Week"]

        # Get a list of batter stats given a player id and the desired time range
        batterStats = self.lg.player_stats(player_id, req_type=time)[0]
        # Set every stat that is not available to 0.0
        batter_keys = list(batterStats.keys())
        for k in batter_keys:
            if batterStats[k] == "-": batterStats[k] = 0
        # Get a list of all details for a batter, primarily used for their team to get their ballpark factor
        pD = self.lg.player_details(int(player_id))
        # Get the players team from our pD object
        playerTeam = pD[0]['editorial_team_full_name']
        playerName = batterStats['name']
        playerAB = batterStats['AB']  # Number of player at-bats
        playerAVG = batterStats['AVG']  # Player's batting average
        playerOPS = batterStats['OPS']  # Player's OBP + Slugging
        playerHR = batterStats['HR']  # Number of home runs hit
        playerBB = batterStats['BB']  # Number of walks
        playerIBB = batterStats['IBB']  # Number of intentional walks
        playerSF = batterStats['SF']  # Number of sacrifice flies
        playerHBP = batterStats['HBP']  # Number of times hit by a pitch
        player1B = batterStats['1B']  # Number of singles
        player2B = batterStats['2B']  # Number of doubles
        player3B = batterStats['3B']  # Number of triples
        playerPA = batterStats['PA']  # Number of plate appearances
        playerSO = batterStats['SO']  # Number of strikeouts
        playerH = batterStats['H']  # Number of hits
        # Set playerWar if type is season, otherwise set to 0 since it is not available
        try:
            playerWAR = batterStats['WAR']
        except Exception as e:
            # print("Failed to get the player's WAR rating. Only available for a players season stats. Not last month or week")
            playerWAR = 0
        # Gets the player's weighted on base average if available using league constants from FanGraphs
        try:
            wOBA = ((self.wBB * playerBB) + (self.wHBP * playerHBP) + (self.w1B * player1B) + (self.w2B * player2B) + (self.w3B * player3B) + (self.wHR * playerHR)) / (playerAB + playerBB - playerIBB + playerSF + playerHBP)
            wOBA = float("{:.3f}".format(wOBA))
        except Exception as e:
            # print("wOBA Error: ", e)
            wOBA = 0
        # Get the player's batting average on balls in play
        try:
            BABIP = (playerH - playerHR) / (playerAB - playerHR - playerSO + playerSF)
            BABIP = float("{:.3f}".format(BABIP))
        except Exception as e:
            # print("BABIP Error: ", e)
            BABIP = 0
        # Gets the player's number of weighted runs scored
        try:
            wRC = (((wOBA - self.obaW) / self.wOBAScale) + self.rPAW) * playerPA
            wRC = float("{:.3f}".format(wRC))
        except Exception as e:
            # print("wRC Error: ", e)
            wRC = 0
        # Gets the player's number of weighted runs created per plate appearance
        try:
            wRCPA = float(wRC) / playerPA
            wRCPA = float("{:.3f}".format(wRCPA))
        except Exception as e:
            # print("wRC/PA Error: ", e)
            wRCPA = 0
        # Gets the player's weighted runs above average which gives us their weighted runs created plus which incorporates ballpark factors
        try:
            # wRAA = ((wOBA – league wOBA) / wOBA scale) × PA
            wRAA = ((wOBA - self.obaW) / self.wOBAScale) * playerPA
            playerParkFactor = self.ballParkDict[playerTeam] / 100
            # wRC+ = (((wRAA/PA + League R/PA) + (League R/PA – Park Factor* League R/PA))/ (AL or NL wRC/PA excluding pitchers))*100
            if playerTeam in self.nlTeamList:
                wRCP = ((((wRAA / playerPA) + self.rPAW) + (self.rPAW - (playerParkFactor * self.rPAW))) / (self.nlWRC / self.nlPA)) * 100
            else:
                wRCP = ((((wRAA / playerPA) + self.rPAW) + (self.rPAW - (playerParkFactor * self.rPAW))) / (self.alWRC / self.alPA)) * 100
            wRCP = float("{:.3f}".format(wRCP))
        except Exception as e:
            # print("wRC+ Error: ", e)
            wRCP = 0
        # Get the players walk and strikeout percentages
        try:
            bb = (playerBB / playerAB) * 100
            bb = float("{:.3f}".format(bb))
        except Exception as e:
            # print("BB Error: ", e)
            bb = 0
        try:
            k = (playerSO / playerAB) * 100
            k = float("{:.3f}".format(k))
        except Exception as e:
            # print("K Error: ", e)
            k = 0
        player_dict = {
            playerName: {
                "PA": playerPA,
                "BB": bb,
                "K": k,
                "BABIP": BABIP,
                "AVG": playerAVG,
                "OPS": playerOPS,
                "wOBA": wOBA,
                "wRC": wRC,
                "wRCPA": wRCPA,
                "wRCP": wRCP
            }
        }
        # If time is season, add WAR to dict, otherwise dont
        if time == "season":
            player_dict[playerName]["WAR"] = playerWAR

        return player_dict

    def get_pitcher(self, time, player_id):
        """
        Function to query a pitcher given an id, with the option for stat desired time range
        :param time: str - "season" || "lastmonth" || "lastweek"
        :param player_id: str - Id of the player to be analyzed
        :return: desired pitcher's stats in the form of a dict
        """
        # Get a list of pitcher stats given player's id and the desired time range
        pitcherStats = self.lg.player_stats(player_id, req_type=time)[0]
        # Set every stat that is not available to 0.0
        for i in pitcherStats:
            if pitcherStats[i] == "-":
                pitcherStats[i] = 0.0
        playerName = pitcherStats['name']
        try:
            playerGames = pitcherStats['G']
            playerIP = pitcherStats['IP']
            playerBF = pitcherStats['BF']  # Number of batters faced
            playerBB = pitcherStats['BB']  # Number of batters walked
            playerKP = pitcherStats['K']  # Number of strikeouts
            playerHR = pitcherStats['HR']  # Number of home runs allowed
            playerHBP = pitcherStats['HBP']  # Number of batters hit with a pitch
            playerERA = pitcherStats['ERA']  # Player's ERA
            playerWHIP = pitcherStats['WHIP']  # Player's WHIP
            playerWin = pitcherStats['W']      # Number of wins
            playerLoss = pitcherStats['L']
            playerSV = pitcherStats['SV']
            try:
                playerWAR = pitcherStats['WAR']
            except Exception as e:
                # print("Failed to get the player's WAR rating. Only available for a players season stats. Not last month or week")
                playerWAR = 0
            # Set strikeouts before it is modified for K%
            strikeouts = playerKP
            try:
                bb = playerBB / playerBF
            except Exception as e:
                # print("BB Error: ", e)
                bb = 0
            try:
                kP = playerKP / playerBF
            except Exception as e:
                # print("K%: ", e)
                kP = 0
            # Multiply BB and KP by 100 to get a percentage and format them
            bb = "{:.3f}".format(bb * 100)
            kP = "{:.3f}".format(kP * 100)
            # Calculate the FIP score if possible
            try:
                FIP = (13 * playerHR + 3 * (playerBB + playerHBP) - 2 * strikeouts) / playerIP
                # Constant is the league average FPI score for year
                FIP = FIP + self.FIP_Constant
            except Exception as e:
                # print("FIP Error: ", e)
                FIP = 0
            FIP = "{:.3f}".format(FIP)
            # If time is season, add WAR to dict, otherwise dont
            playerDict = {
                playerName:
                    {
                        "ID": player_id,
                        "GP": playerGames,
                        "IP": playerIP,
                        "BF": playerBF,
                        "BB": bb,
                        "SO%": kP,
                        "FIP": FIP,
                        "ERA": playerERA,
                        "WHIP": playerWHIP,
                        "K": strikeouts,
                        "HR": playerHR,
                        "W": playerWin,
                        "L": playerLoss,
                        "SV": playerSV
                    }
            }
            # If time is season, add WAR to dict, otherwise dont
            if time == "season":
                playerDict[playerName]["WAR"] = playerWAR
            return playerDict
        except:
            playerDict = {
                playerName:
                    {
                        "ID": player_id,
                        "GP": 0.0,
                        "IP": 0.0,
                        "BF": 0.0,
                        "BB": 0.0,
                        "SO%": 0.0,
                        "FIP": 0.0,
                        "ERA": 0.0,
                        "WHIP": 0.0,
                        "K": 0.0,
                        "HR": 0.0,
                        "W": 0.0,
                        "L": 0.0,
                        "SV": 0.0
                    }
            }
            return playerDict

    def get_pitchers(self, time, status, qualified):
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
            for i in self.lg.taken_players():
                if i["position_type"] == "P":
                    takenPID.append(i["player_id"])
            for i in self.lg.free_agents('P'):
                faPID.append(i["player_id"])
            for i in self.tm.roster(self.lg.current_week()):
                if i["position_type"] == "P":
                    teamPID.append(i["player_id"])
            allPID.append(takenPID)
            allPID.append(faPID)
            allPID.append(teamPID)
        # Add every taken pitcher to allPID
        elif status == 1:
            for i in self.lg.taken_players():
                if i["position_type"] == "P":
                    takenPID.append(i["player_id"])
            allPID.append(takenPID)
        # Add every FA pitcher to allPID
        elif status == 2:
            for i in self.lg.free_agents('P'):
                faPID.append(i["player_id"])
            allPID.append(faPID)
        # Add every pitcher on your team to allPID
        else:
            for i in self.tm.roster(self.lg.current_week()):
                if i["position_type"] == "P":
                    teamPID.append(i["player_id"])
            allPID.append(teamPID)

        # For every different list within allPID (up to 3: taken, fa, roster)
        for i in range(0, len(allPID)):
            # Get a list of pitcher stats given a list of player ids and the desired time range
            pitcherStats = self.lg.player_stats(allPID[i], req_type=time)
            for j in range(0, len(pitcherStats)):
                pitcher = pitcherStats[j]
                # Set every stat that is not available to 0.0
                pitcher_keys = list(pitcher.keys())
                for k in pitcher_keys:
                    if pitcher[k] == "-": pitcher[k] = 0
                playerName = pitcher['name']
                playerID = pitcher['player_id']
                playerGames = pitcher['G']
                playerIP = pitcher['IP']
                playerBF = pitcher['BF']  # Number of batters faced
                if qualified:
                    if time == "season":
                        bfQualifier = self.__configs["batters_faced_season"]
                    elif time == "lastmonth":
                        bfQualifier = self.__configs["batters_faced_month"]
                    else:
                        bfQualifier = self.__configs["batters_faced_week"]
                else:
                    bfQualifier = 0
                if float(int(playerBF)) >= bfQualifier:
                    playerBB = pitcher['BB']  # Number of batters walked
                    playerKP = pitcher['K']  # Number of strikeouts
                    playerHR = pitcher['HR']  # Number of home runs allowed
                    playerHBP = pitcher['HBP']  # Number of batters hit with a pitch
                    playerERA = pitcher['ERA']  # Player's ERA
                    playerWHIP = pitcher['WHIP']  # Player's WHIP
                    playerWin = pitcher['W']  # Number of wins
                    playerLoss = pitcher['L']
                    playerSV = pitcher['SV']
                    try:
                        playerWAR = pitcher['WAR']
                    except Exception as e:
                        # print("Failed to get the player's WAR rating. Only available for a players season stats. Not last month or week")
                        playerWAR = 0
                    # Set strikeouts before it is modified for K%
                    strikeouts = playerKP
                    try:
                        bb = playerBB / playerBF
                    except Exception as e:
                        # print("BB Error: ", e)
                        bb = 0
                    try:
                        kP = playerKP / playerBF
                    except Exception as e:
                        # print("K%: ", e)
                        kP = 0
                    # Multiply BB and KP by 100 to get a percentage and format them
                    bb = "{:.3f}".format(bb * 100)
                    kP = "{:.3f}".format(kP * 100)
                    # Calculate the FIP score if possible
                    try:
                        FIP = (13 * playerHR + 3 * (playerBB + playerHBP) - 2 * strikeouts) / playerIP
                        # Constant is the league average FPI score for year
                        FIP = FIP + self.FIP_Constant
                    except Exception as e:
                        # print("FIP Error: ", e)
                        FIP = 0
                    FIP = "{:.3f}".format(FIP)
                    playerDict = {
                        playerName:
                        {
                            "ID": playerID,
                            "GP": playerGames,
                            "IP": playerIP,
                            "BF": playerBF,
                            "BB": bb,
                            "SO%": kP,
                            "FIP": FIP,
                            "ERA": playerERA,
                            "WHIP": playerWHIP,
                            "K": strikeouts,
                            "HR": playerHR,
                            "W": playerWin,
                            "L": playerLoss,
                            "SV": playerSV
                        }
                    }
                    # If time is season, add WAR to dict, otherwise dont
                    if time == "season":
                        playerDict[playerName]["WAR"] = playerWAR
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

    def get_all_players(self, time, qualified):

        """
        Displays every single player in the yahoo league based on the time period
        and determines whether players need to meet certain qualifications to be considered
        :param time: str - "season" || "lastmonth" || "lastweek"
        :param qualified: bool - Whether or not to include only 'qualified' players based on the time
        period selected
        :return:
        """
        teamPitchers = self.get_pitchers(time, 3, qualified)
        teamBatters = self.get_batters(time, 3, qualified)

        print("All pitchers currently on your team:")
        self.print_pitchers(teamPitchers, False)

        print("All batters currently on your team:")
        self.print_batters(teamBatters, True)

        takenPitchers = self.get_pitchers(time, 1, qualified)
        takenBatters = self.get_batters(time, 1, qualified)

        print("All pitchers currently on teams:")
        self.print_pitchers(takenPitchers, False)

        print("All batters currently on teams:")
        self.print_batters(takenBatters, True)

        faPitchers = self.get_pitchers(time, 2, qualified)
        faBatters = self.get_batters(time, 2, qualified)

        print("All free-agent pitchers")
        self.print_pitchers(faPitchers, False)

        print("All free-agent batters")
        self.print_batters(faBatters, True)

    def pitcher_career_stats(self, player_name):
        """
        Return's a pitcher's career statistics given a name
        :param player_name: str - Name of player to be analyzed
        :return:
        """
        playerID = statsapi.lookup_player(player_name)[0]['id']
        playerCareer = statsapi.player_stat_data(playerID, 'pitching', 'career')
        # Set every stat that is not available to 0.0
        for i in list(playerCareer['stats'][0]['stats'].keys()):
            if playerCareer['stats'][0]['stats'][i] == "-":
                playerCareer['stats'][0]['stats'][i] = 0.0
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
        # Set strikeouts before it is modified for K%
        strikeouts = playerKP
        try:
            bb = float(playerBB) / float(playerBF)
        except Exception as e:
            print("BB Error: ", e)
            bb = 0
        try:
            kP = float(playerKP) / float(playerBF)
        except Exception as e:
            print("K%: ", e)
            kP = 0
        # Multiply BB and KP by 100 to get a percentage and format them
        bb = "{:.3f}".format(bb * 100)
        kP = "{:.3f}".format(kP * 100)
        # Calculate the FIP score if possible
        try:
            FIP = (13 * playerHR + 3 * (playerBB + playerHBP) - 2 * strikeouts) / float(playerIP)
            # Constant is the league average FPI score for year
            FIP = FIP + self.FIP_Constant
        except Exception as e:
            print("FIP Error: ", e)
            FIP = 0
        FIP = "{:.3f}".format(FIP)
        # Return the desired pitcher
        try:
            playerDict = {
                player_name:
                    {
                        "GP": playerGames,
                        "IP": playerIP,
                        "BF": playerBF,
                        "BB": bb,
                        "SO%": kP,
                        "FIP": FIP,
                        "ERA": playerERA,
                        "WHIP": playerWHIP,
                        "K": strikeouts,
                        "HR": playerHR,
                        "W": playerWin,
                        "L": playerLoss,
                        "SV": playerSV
                    }
            }
        except:
            playerDict = {
                player_name:
                    {
                        "GP": 0.0,
                        "IP": 0.0,
                        "BF": 0.0,
                        "BB": 0.0,
                        "SO%": 0.0,
                        "FIP": 0.0,
                        "ERA": 0.0,
                        "WHIP": 0.0,
                        "K": 0.0,
                        "HR": 0.0,
                        "W": 0.0,
                        "L": 0.0,
                        "SV": 0.0
                    }
            }
        playerDict[player_name]["ID"] = playerID
        return playerDict

    def batter_career_stats(self, player_name):
        """
        Return's a batter's career statistics given a name
        :param player_name: str - Name of player to be analyzed
        :return:
        """
        playerID = statsapi.lookup_player(player_name)[0]['id']
        playerTeam = statsapi.lookup_player(player_name)[0]['currentTeam']['id']
        playerTeam = statsapi.get('team', {'teamId': playerTeam})['teams'][0]['name']

        playerCareer = statsapi.player_stat_data(playerID, 'hitting', 'career')
        # Set every stat that is not available to 0.0
        for i in list(playerCareer['stats'][0]['stats'].keys()):
            if playerCareer['stats'][0]['stats'][i] == "-":
                playerCareer['stats'][0]['stats'][i] = 0.0
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
        # Gets the player's weighted on base average if available using league constants from FanGraphs
        try:
            wOBA = ((self.wBB * playerBB) + (self.wHBP * playerHBP) + (self.w1B * player1B) + (self.w2B * player2B) + (self.w3B * player3B) + (self.wHR * playerHR)) / (playerAB + playerBB - playerIBB + playerSF + playerHBP)
            wOBA = float("{:.3f}".format(wOBA))
        except Exception as e:
            print("wOBA Error: ", e)
            wOBA = 0

        # Get the player's batting average on balls in play
        try:
            BABIP = (playerH - playerHR) / (playerAB - playerHR - playerSO + playerSF)
            BABIP = float("{:.3f}".format(BABIP))
        except Exception as e:
            print("BABIP Error: ", e)
            BABIP = 0

        # Gets the player's number of weighted runs scored
        try:
            wRC = (((wOBA - self.obaW) / self.wOBAScale) + self.rPAW) * playerPA
            wRC = float("{:.3f}".format(wRC))
        except Exception as e:
            print("wRC Error: ", e)
            wRC = 0
        # Gets the player's number of weighted runs created per plate appearance
        try:
            wRCPA = wRC / playerPA
            wRCPA = float("{:.3f}".format(wRCPA))
        except Exception as e:
            print("wRC/PA Error: ", e)
            wRCPA = 0
        # Gets the player's weighted runs above average which gives us their weighted runs created plus which incorporates ballpark factors
        try:
            # wRAA = ((wOBA – league wOBA) / wOBA scale) × PA
            wRAA = ((wOBA - self.obaW) / self.wOBAScale) * playerPA
            playerParkFactor = self.ballParkDict[playerTeam] / 100
            # wRC+ = (((wRAA/PA + League R/PA) + (League R/PA – Park Factor* League R/PA))/ (AL or NL wRC/PA excluding pitchers))*100
            if playerTeam in self.nlTeamList:
                wRCP = ((((wRAA / playerPA) + self.rPAW) + (self.rPAW - (playerParkFactor * self.rPAW))) / (
                            self.nlWRC / self.nlPA)) * 100
            else:
                wRCP = ((((wRAA / playerPA) + self.rPAW) + (self.rPAW - (playerParkFactor * self.rPAW))) / (
                            self.alWRC / self.alPA)) * 100
            wRCP = float("{:.3f}".format(wRCP))
        except Exception as e:
            print("wRC+ Error: ", e)
            wRCP = 0
        # Get the players walk and strikeout percentages
        try:
            bb = (playerBB / playerAB) * 100
            bb = "{:.3f}".format(bb)
        except Exception as e:
            # print("BB Error: ", e)
            bb = 0
        try:
            k = (playerSO / playerAB) * 100
            k = "{:.3f}".format(k)
        except Exception as e:
            # print("K Error: ", e)
            k = 0
        # Return the desired player
        player_dict = {
            player_name: {
                "PA": playerPA,
                "BB": bb,
                "K": k,
                "BABIP": BABIP,
                "AVG": playerAVG,
                "OPS": playerOPS,
                "wOBA": wOBA,
                "wRC": wRC,
                "wRCPA": wRCPA,
                "wRCP": wRCP
            }
        }
        return player_dict

    def outlier(self, player_name, status):
        """
        Displays whether a player is currently over or under-achieving
        comparing their current season statistics with their career statistics
        :param player_name: str - Name of player to be analyzed
        :param status: int - 0 == batter, 1 == pitcher
        :return:
        """
        try:
            currentSeasonStats = self.get_player(player_name, "season")
            over_categories = []
            under_categories = []
            if status == 0:
                careerStats = self.batter_career_stats(player_name)
                print("Current Season Stats")
                self.print_batters(currentSeasonStats, reverse=True)
                print("Career Stats")
                self.print_batters(careerStats, reverse=True)
                currentWRCPA = float(currentSeasonStats[player_name]["wRCPA"])
                currentWOBA = float(currentSeasonStats[player_name]["wOBA"])
                currentWRCP = float(currentSeasonStats[player_name]["wRCP"])
                currentBABIP = float(currentSeasonStats[player_name]["BABIP"])
                careerWRCPA = float(careerStats[player_name]["wRCPA"])
                careerWOBA = float(careerStats[player_name]["wOBA"])
                careerWRCP = float(careerStats[player_name]["wRCP"])
                careerBABIP = float(careerStats[player_name]["BABIP"])
                if currentWRCPA > careerWRCPA:
                    diff = currentWRCPA - careerWRCPA
                    diff = "{:.3f}".format(diff)
                    over_categories.append("wRC/PA")
                    print("Up " + str(diff) + " points in wRC/PA")
                else:
                    diff = careerWRCPA - currentWRCPA
                    diff = "{:.3f}".format(diff)
                    under_categories.append("wRC/PA")
                    print("Down " + str(diff) + " points in wRC/PA")
                if currentWOBA > careerWOBA:
                    diff = currentWOBA - careerWOBA
                    diff = "{:.3f}".format(diff)
                    over_categories.append("wOBA")
                    print("Up " + str(diff) + " points in wOBA")
                else:
                    diff = careerWOBA - currentWOBA
                    diff = "{:.3f}".format(diff)
                    under_categories.append("wOBA")
                    print("Down " + str(diff) + " points in wOBA")
                if currentWRCP > careerWRCP:
                    diff = currentWRCP - careerWRCP
                    diff = "{:.3f}".format(diff)
                    over_categories.append("wRC+")
                    print("Up " + str(diff) + " points in wRC+")
                else:
                    diff = careerWRCP - currentWRCP
                    diff = "{:.3f}".format(diff)
                    under_categories.append("wRC+")
                    print("Down " + str(diff) + " points in wRC+")
                if currentBABIP > careerBABIP:
                    diff = currentBABIP - careerBABIP
                    diff = "{:.3f}".format(diff)
                    over_categories.append("BABIP")
                    print("Up " + str(diff) + " points in BABIP")
                else:
                    diff = careerBABIP - currentBABIP
                    diff = "{:.3f}".format(diff)
                    under_categories.append("BABIP")
                    print("Down " + str(diff) + " points in BABIP")
            else:
                careerStats = self.pitcher_career_stats(player_name)
                print("Current Season Stats")
                self.print_pitchers(currentSeasonStats, reverse=True)
                print("Career Stats")
                self.print_pitchers(careerStats, reverse=True)
                currentFIP = float(currentSeasonStats[player_name]['FIP'])
                currentERA = float(currentSeasonStats[player_name]['ERA'])
                currentWHIP = float(currentSeasonStats[player_name]['WHIP'])
                currentKP = float(currentSeasonStats[player_name]['SO%'])
                currentBP = float(currentSeasonStats[player_name]['BB'])

                careerFIP = float(careerStats[player_name]['FIP'])
                careerERA = float(careerStats[player_name]['ERA'])
                careerWHIP = float(careerStats[player_name]['WHIP'])
                careerKP = float(careerStats[player_name]['SO%'])
                careerBP = float(careerStats[player_name]['BB'])

                if currentFIP < careerFIP:
                    diff = careerFIP - currentFIP
                    diff = "{:.3f}".format(diff)
                    over_categories.append("FIP")
                    print("Down " + str(diff) + " points in FIP")
                else:
                    diff = currentFIP - careerFIP
                    diff = "{:.3f}".format(diff)
                    under_categories.append("FIP")
                    print("Up " + str(diff) + " points in FIP")
                if currentERA < careerERA:
                    diff = careerERA - currentERA
                    diff = "{:.3f}".format(diff)
                    over_categories.append("ERA")
                    print("Down " + str(diff) + " points in ERA")
                else:
                    diff = currentERA - careerERA
                    diff = "{:.3f}".format(diff)
                    under_categories.append("ERA")
                    print("Up " + str(diff) + " points in ERA")
                if currentWHIP < careerWHIP:
                    diff = careerWHIP - currentWHIP
                    diff = "{:.3f}".format(diff)
                    over_categories.append("WHIP")
                    print("Down " + str(diff) + " points in WHIP")
                else:
                    diff = currentWHIP - careerWHIP
                    diff = "{:.3f}".format(diff)
                    under_categories.append("WHIP")
                    print("Up " + str(diff) + " points in WHIP")
                if currentKP > careerKP:
                    diff = currentKP - careerKP
                    diff = "{:.3f}".format(diff)
                    over_categories.append("K%")
                    print("Up " + str(diff) + " points in K%")
                else:
                    diff = careerKP - currentKP
                    diff = "{:.3f}".format(diff)
                    under_categories.append("K%")
                    print("Down " + str(diff) + " points in K%")
                if currentBP < careerBP:
                    diff = careerBP - currentBP
                    diff = "{:.3f}".format(diff)
                    over_categories.append("BB%")
                    print("Down " + str(diff) + " points in BB%")
                else:
                    diff = currentBP - careerBP
                    diff = "{:.3f}".format(diff)
                    under_categories.append("BB%")
                    print("Up " + str(diff) + " points in BB%")
            print(f"Currently overachieving in the following categories: {over_categories}")
            print(f"Currently underacheiving in the following categories: {under_categories}")
        except Exception as e:
            print("Did you correctly call the function? (i.e. not using the 'status' parameter correctly)")
            print("Error: ", e)

    def whos_hot(self, time):
        """
        Displays the 10 best qualified free agent / taken pitchers and batters
        over the desired time period based on FIP and WRC+
        :param time: str - "season" || "lastmonth" || "lastweek"
        :return:
        """
        # Print top 10 pitcher free agents and taken players
        ttRP = self.get_pitchers(time, 1, qualified=True)
        hotPList = dict(sorted(ttRP.items(), key=lambda item: item[1]['FIP'])[0:10])
        print("\n" + "Top 10 Hottest Rostered Pitchers: ")
        self.print_pitchers(hotPList, reverse=False)

        ttFAP = self.get_pitchers(time, 2, qualified=True)
        hotPList2 = dict(sorted(ttFAP.items(), key=lambda item: item[1]['FIP'])[0:10])
        print("\n" + "Top 10 Hottest Free Agent Pitchers: ")
        self.print_pitchers(hotPList2, reverse=False)

        # Print top 10 batter free agents and taken players
        ttRB = self.get_batters(time, 1, qualified=True)
        hotBList = dict(sorted(ttRB.items(), key=lambda item: item[1]['wRCP'], reverse=True)[0:10])
        print("\n" + "Top 10 Hottest Rostered Batters: ")
        self.print_batters(hotBList, reverse=True)

        ttFAB = dict(list(self.get_batters(time, 2, qualified=True).items()))
        hotBList2 = dict(sorted(ttFAB.items(), key=lambda item: item[1]['wRCP'], reverse=True)[0:10])
        print("\n" + "Top 10 Hottest Free Agent Batters: ")
        self.print_batters(hotBList2, reverse=True)

    def whos_cold(self, time):
        """
        Displays the 10 worst qualified free agent / taken pitchers and batters
        over the desired time period based on FIP and WRC+
        :param time: str - "season" || "lastmonth" || "lastweek"
        :return:
        """
        # Print top 10 worst pitcher free agents and taken players
        ttRP = self.get_pitchers(time, 1, qualified=True)
        coldPList = dict(sorted(ttRP.items(), key=lambda item: item[1]['FIP'], reverse=True)[0:10])
        print("\n" + "Top 10 Coldest Rostered Pitchers: ")
        self.print_pitchers(coldPList, reverse=True)

        ttFAP = self.get_pitchers(time, 2, qualified=True)
        coldPList2 = dict(sorted(ttFAP.items(), key=lambda item: item[1]['FIP'], reverse=True)[0:10])
        print("\n" + "Top 10 Coldest Free Agent Pitchers: ")
        self.print_pitchers(coldPList2, reverse=True)

        # Print top 10 worst batter free agents and taken players
        ttRB = self.get_batters(time, 1, qualified=True)
        coldBList = dict(sorted(ttRB.items(), key=lambda item: item[1]['wRCP'])[0:10])
        print("\n" + "Top 10 Coldest Rostered Batters: ")
        self.print_batters(coldBList, reverse=False)

        ttFAB = self.get_batters(time, 2, qualified=True)
        coldBList2 = dict(sorted(ttFAB.items(), key=lambda item: item[1]['wRCP'])[0:10])
        print("\n" + "Top 10 Coldest Free Agent Batters: ")
        self.print_batters(coldBList2, reverse=False)
