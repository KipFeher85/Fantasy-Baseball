================================================
Yahoo Fantasy Baseball Statistic Analysis Module
================================================

Python Module Usage
-------------------

::

  In [1]: from yahoo_oauth import OAuth2
  
  In [2]: import yahoo_fantasy_api as yfa

  In [3]: import json

  In [4]: import statsapi
  
  In [5]: import yahoo_fb_stat_analysis as yfbsa
  
  In [6]: oauth = OAuth2(None, None, from_file='OAuth2.json')
  [2021-06-18 15:39:52,655 DEBUG] [yahoo_oauth.oauth.__init__] Checking
  [2021-06-18 15:39:52,656 DEBUG] [yahoo_oauth.oauth.token_is_valid] ELAPSED TIME : 3514.6330070495605
  [2021-06-18 15:39:52,656 DEBUG] [yahoo_oauth.oauth.token_is_valid] TOKEN IS STILL VALID
  
  In [7]: gm = yfa.Game(oauth, 'mlb')
  
  In [8]: leagueID = gm.league_ids(year=2021)[0]
  Out[8]: ['NNN.a.NNNN']
  
  In [9]: lg = gm.to_league(leagueID)
  
  In [10]: tm = lg.to_team(team_key=lg.team_key())
  
  In [11]: lgObj = League()

  In [12]: lgObj.getCurrentRoster()
  Out[12]:
  Hitter List:
  {'player_id': 9718, 'name': 'J.T. Realmuto', 'status': '', 'position_type': 'B', 'eligible_positions': ['C', 'Util'], 'selected_position': 'C'}
  {'player_id': 8967, 'name': 'Paul Goldschmidt', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', 'Util'], 'selected_position': '1B'}
  ....
  {'player_id': 10439, 'name': 'Eloy Jiménez', 'status': 'IL60', 'position_type': 'B', 'eligible_positions': ['OF', 'Util', 'IL'], 'selected_position': 'IL'}
  Pitcher List:
  {'player_id': 11903, 'name': 'Luis Garcia', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'SP'}
  {'player_id': 9122, 'name': 'Trevor Bauer', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'SP'}
  ....
  {'player_id': 12205, 'name': 'Sammy Long', 'status': '', 'position_type': 'P', 'eligible_positions': ['RP', 'P'], 'selected_position': ''}
  Injured List:
  {'player_id': 11568, 'name': 'Jake Fraley', 'status': 'DTD', 'position_type': 'B', 'eligible_positions': ['OF', 'Util'], 'selected_position': 'OF'}
  {'player_id': 9606, 'name': 'Max Muncy', 'status': 'IL10', 'position_type': 'B', 'eligible_positions': ['1B', '2B', '3B', 'Util', 'IL'], 'selected_position': 'IL'}
  ....
  {'player_id': 10932, 'name': 'Sixto Sánchez', 'status': 'NA', 'position_type': 'P', 'eligible_positions': ['SP', 'P', 'NA'], 'selected_position': 'NA'}

  In [13]: lgObj.currentRosterStats('lastmonth')
  Out[13]:
  Your batters:
  Name: Jake Fraley PA: 83.0 wRC: 17.273 wRC/PA: 0.208 wOBA: 0.422 BABIP: 0.306 WAR: 0.3 wRC+: 100.44673175922586
  Name: Max Muncy PA: 244.0 wRC: 49.796 wRC/PA: 0.204 wOBA: 0.417 BABIP: 0.287 WAR: 0.8 wRC+: 97.19561995027043
  ....
  Name: Eloy Jiménez PA: 0 wRC: -0.0 wRC/PA: 0.0 wOBA: 0.0 BABIP: 0.0 WAR: 0.0 wRC+: 0.0
  Your pitchers:
  Name: Sixto Sánchez GS: - IP: 0 BF: 0 BB%: 0.00 K%: 0.00 FIP: 0.00 ERA: - WHIP: - WAR: 0.0
  Name: Sammy Long GS: 2.0 IP: 9.0 BF: 34.0 BB%: 5.88 K%: 29.41 FIP: 1.58 ERA: 5.0 WHIP: 0.89 WAR: 0.3
  ....
  Name: Alek Manoah GS: 4.0 IP: 20.1 BF: 83.0 BB%: 9.64 K%: 25.30 FIP: 4.33 ERA: 2.66 WHIP: 1.08 WAR: 0.3

  In [14]: lgObj.teamDetails()
  Out[14]:
  [('team_key', 'team's key'), ('team_id', '10'), ('name', 'Vlad Jr for MVP'), ('url', 'team url'), ('team_logos', [{'team_logo': {'size': 'large', 'url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/44fd8e00d7bbf781b3b7b4ca468a4072986c485ee4f0b8cd083b47ad327c42e3.png'}}]), ('waiver_priority', 10), ('number_of_moves', '21'), ('number_of_trades', 0), ('roster_adds', {'coverage_type': 'week', 'coverage_value': 11, 'value': '1'}), ('league_scoring_type', 'head'), ('draft_position', 2), ('has_draft_grade', 0), ('managers', [{'manager': {'manager_id': '10', 'nickname': 'Mr. X', 'guid': 'B3QNT4MWWQDXZS3J7HDPCDPWVU', 'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg', 'felo_score': '658', 'felo_tier': 'silver'}}])]
  [('team_key', 'team's key'), ('team_id', '12'), ('name', 'Pirates Suck'), ('url', 'team url'), ('team_logos', [{'team_logo': {'size': 'large', 'url': 'https://s.yimg.com/cv/apiv2/default/mlb/mlb_4_s.png'}}]), ('waiver_priority', 12), ('number_of_moves', '16'), ('number_of_trades', 0), ('roster_adds', {'coverage_type': 'week', 'coverage_value': 11, 'value': '0'}), ('league_scoring_type', 'head'), ('draft_position', 3), ('has_draft_grade', 0), ('managers', [{'manager': {'manager_id': '12', 'nickname': 'Mr. Y', 'guid': 'JLUKFLTAHXRTWF46MW3YLFKE3E', 'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg', 'felo_score': '668', 'felo_tier': 'silver'}}])]
  ....
  [('team_key', 'team's key'), ('team_id', '2'), ('name', 'A Bunch of Dumbo’s'), ('url', 'team url'), ('team_logos', [{'team_logo': {'size': 'large', 'url': 'https://s.yimg.com/cv/apiv2/default/mlb/mlb_2.png'}}]), ('waiver_priority', 1), ('number_of_moves', '1'), ('number_of_trades', 0), ('roster_adds', {'coverage_type': 'week', 'coverage_value': 11, 'value': '0'}), ('league_scoring_type', 'head'), ('draft_position', 12), ('has_draft_grade', 0), ('managers', [{'manager': {'manager_id': '2', 'nickname': 'Mr. Z', 'guid': '7NIG4ZRBEELFHB43MOYUGCW3KU', 'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg', 'felo_score': '477', 'felo_tier': 'bronze'}}])]

  In [15]: lgObj.predictTeamDay()
  Out[15]:
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] URL: https://statsapi.mlb.com/api/{ver}/schedule
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] Found query param: sportId
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] Found query param: hydrate
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] path_params: {}
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] query_params: {'sportId': '1', 'hydrate': 'decisions,probablePitcher(note),linescore'}
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] Replacing {ver} with default: v1.
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] URL: https://statsapi.mlb.com/api/v1/schedule
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] Adding query parameter sportId=1
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] URL: https://statsapi.mlb.com/api/v1/schedule?sportId=1
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] Adding query parameter hydrate=decisions,probablePitcher(note),linescore
  [2021-06-18 16:19:48,422 DEBUG] [statsapi.__init__.get] URL: https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=decisions,probablePitcher(note),linescore
  Home Pitcher stats over the past month:
  Team: New York Yankees HP: Jameson Taillon
  IP: 11.1 BF: 42.0 BB%: 11.9 K%: 28.57 FIP: 2.32 ERA: 0.79 WHIP: 0.88 K: 12.0 HR: 0.0
  Note: Taillon had a forgettable start Saturday against the Phillies, as he recorded only one out while allowing four runs on five hits. He will look to put that in the rear-view mirror in his first career start against the A's.
  Team: Atlanta Braves HP: Max Fried
  IP: 22.0 BF: 84.0 BB%: 4.76 K%: 25.0 FIP: 2.5 ERA: 4.5 WHIP: 0.95 K: 21.0 HR: 1.0
  Note: Fried allowed a pair of home runs during Saturday's loss in Miami. He had allowed just one homer over his past six starts combined.
  ....
  Team: Houston Astros HP: Luis Garcia
  IP: 15.2 BF: 72.0 BB%: 9.72 K%: 16.67 FIP: 3.99 ERA: 5.74 WHIP: 1.6 K: 12.0 HR: 1.0
  Note: Garcia had won five consecutive starts before giving up four runs (three earned) in 4 1/3 innings in last Saturday's loss to the Twins. As a starter, he has a 3.14 ERA and 1.06 WHIP in 57 1/3 innings.

  Away Pitcher stats over the past month:
  Team: New York Mets AP: Joey Lucchesi
  IP: 29.0 BF: 118.0 BB%: 7.63 K%: 37.29 FIP: 1.58 ERA: 0.0 WHIP: 1.1 K: 44.0 HR: 1.0
  Note: Despite Lucchesi's recent success -- a 1.56 ERA over his last four starts -- the Mets still aren't letting him face opposing batters more than twice. Perhaps that will change after he set season highs with five innings and 72 pitches last time out.
  Team: Cleveland Indians AP: J.C. Mejia
  IP: 12.2 BF: 49.0 BB%: 10.2 K%: 26.53 FIP: 2.23 ERA: 0.0 WHIP: 1.18 K: 13.0 HR: 0.0
  Note: Mejía will work on short rest after being pulled from his last outing after four innings to preserve his pitch count. The Indians are trying to be creative to get through their lack of starters, and Mejía will likely remain around the 50-60 pitch count.
  ....
  Team: Oakland Athletics AP: James Kaprielian
  IP: 30.0 BF: 121.0 BB%: 5.79 K%: 36.36 FIP: 3.07 ERA: 0.79 WHIP: 1.07 K: 44.0 HR: 5.0
  Note: Kaprielian is off to a strong start with a 2.51 ERA through his first six big league starts. The rookie has been particularly tough against right-handed batters, holding them to a .131 batting average.

  In [16]: faBatters = lgObj.getBatters('lastmonth', 2)
  Out[16]: {'Albert Pujols': [63.0, 5.0, 16.667, 0.267, 0.283, 0.884, 0.376, 10.779, 0.0, 97.58016735667573, 0.171] .... }

  In [17]: lgObj.printBatters('lastmonth', faBatters)
  Out[17]:
  Name: Luis Torrens PA: 9.0 wRC: 3.835 wRC/PA: 0.426 wOBA: 0.693 BABIP: 0.333 wRC+: 127.42872648942306
  Name: Luis Rengifo PA: 4.0 wRC: 0.897 wRC/PA: 0.224 wOBA: 0.442 BABIP: 0.667 wRC+: 118.29968811199949
  Name: Tony Kemp PA: 85.0 wRC: 16.321 wRC/PA: 0.192 wOBA: 0.402 BABIP: 0.345 wRC+: 100.27186961063333
  Name: Kyle Lewis PA: 49.0 wRC: 7.359 wRC/PA: 0.15 wOBA: 0.35 BABIP: 0.345 wRC+: 100.0976742096935
  ....
  Name: Derek Fisher PA: 2.0 wRC: -0.263 wRC/PA: -0.132 wOBA: 0.0 BABIP: 0.0 wRC+: -5.554554043537899

  In [18]: goldy = lgObj.getBatter('season', 8967)
  Out[18]: {'Paul Goldschmidt': [284.0, 8.915, 24.806, 0.296, 0.248, 0.72, 0.315, 34.654, 0.9, 96.00683997825512, 0.122]}

  In [19]: takenPitchers = lgObj.getPitchers('lastmonth', 1)
  Out[19]: {'Trevor Bauer': [9122.0, 14.0, 88.2, 351.0, 8.26, 31.62, 3.77, 2.64, 0.95, 1.2, 111.0, 14.0]}

  In [20]: lgObj.printPitchers('lastmonth', takenPitchers)
  Out[20]:
  Name: Edwin Díaz GS: 10.0 IP: 9.2 BF: 35.0 BB%: 2.86 K%: 45.71 FIP: -0.02 ERA: 0.93 WHIP: 0.62
  Name: Jacob deGrom GS: 5.0 IP: 27.0 BF: 91.0 BB%: 1.10 K%: 50.55 FIP: 0.32 ERA: 0.33 WHIP: 0.37
  Name: Corbin Burnes GS: 5.0 IP: 29.0 BF: 118.0 BB%: 7.63 K%: 37.29 FIP: 1.58 ERA: 3.1 WHIP: 1.1
  Name: Kevin Gausman GS: 6.0 IP: 36.0 BF: 132.0 BB%: 5.30 K%: 33.33 FIP: 1.99 ERA: 1.0 WHIP: 0.67
  ....
  Name: Zac Gallen GS: 1.0 IP: 2.2 BF: 14.0 BB%: 7.14 K%: 21.43 FIP: 9.04 ERA: 13.5 WHIP: 1.88

  In [21]: bauer = lgObj.getPitcher('season', 9122)
  Out[21]: {'Trevor Bauer': [9122.0, 14.0, 88.2, 351.0, 8.26, 31.62, 3.77, 2.64, 0.95, 1.2, 111.0, 14.0]}

  In [22]: lgObj.getAllPlayers('season')
  Out[22]:
  All pitchers currently on your team:
  Name: Max Scherzer GS: 13.0 IP: 77.1 BF: 289.0 BB%: 5.19 K%: 35.99 FIP: 3.03 ERA: 2.21 WHIP: 0.81 WAR: 1.9
  Name: Kyle Gibson GS: 13.0 IP: 77.2 BF: 307.0 BB%: 7.17 K%: 19.87 FIP: 3.33 ERA: 2.09 WHIP: 1.03 WAR: 1.6
  Name: Daniel Bard GS: 26.0 IP: 28.0 BF: 126.0 BB%: 8.73 K%: 28.57 FIP: 3.35 ERA: 3.86 WHIP: 1.46 WAR: 0.4
  ....
  Name: Alek Manoah GS: 4.0 IP: 20.1 BF: 83.0 BB%: 9.64 K%: 25.30 FIP: 4.33 ERA: 2.66 WHIP: 1.08 WAR: 0.3

  All pitchers currently on teams:
  Name: Josh Hader GS: 28.0 IP: 27.2 BF: 103.0 BB%: 9.71 K%: 46.60 FIP: 0.71 ERA: 0.65 WHIP: 0.76 WAR: 1.2
  Name: Jacob deGrom GS: 11.0 IP: 67.0 BF: 232.0 BB%: 3.45 K%: 47.84 FIP: 0.76 ERA: 0.54 WHIP: 0.51 WAR: 3.8
  Name: Corbin Burnes GS: 11.0 IP: 63.1 BF: 246.0 BB%: 4.07 K%: 41.46 FIP: 0.98 ERA: 2.27 WHIP: 0.85 WAR: 3.4
  ....
  Name: Stephen Strasburg GS: 5.0 IP: 21.2 BF: 95.0 BB%: 14.74 K%: 22.11 FIP: 5.73 ERA: 4.57 WHIP: 1.38 WAR: 0.0

  All free-agent pitchers
  Name: Justin Miller GS: 1.0 IP: 0.2 BF: 2.0 BB%: 0.00 K%: 50.00 FIP: -6.87 ERA: 0.0 WHIP: 0.0 WAR: 0.0
  Name: Spencer Patton GS: 4.0 IP: 4.0 BF: 13.0 BB%: 0.00 K%: 46.15 FIP: 0.13 ERA: 0.0 WHIP: 0.25 WAR: 0.2
  Name: Seth Lugo GS: 6.0 IP: 7.2 BF: 30.0 BB%: 6.67 K%: 40.00 FIP: 0.63 ERA: 1.17 WHIP: 1.17 WAR: 0.3
  ....
  Name: Kyle Freeland GS: 5.0 IP: 20.2 BF: 106.0 BB%: 10.38 K%: 11.32 FIP: 9.67 ERA: 9.58 WHIP: 2.27 WAR: -0.5

  All batters currently on your team:
  Name: Jake Fraley PA: 83.0 wRC: 17.273 wRC/PA: 0.208 wOBA: 0.422 BABIP: 0.306 WAR: 0.3 wRC+: 100.44673175922586
  Name: Max Muncy PA: 244.0 wRC: 49.796 wRC/PA: 0.204 wOBA: 0.417 BABIP: 0.287 WAR: 0.8 wRC+: 97.19561995027043
  Name: Jose Altuve PA: 271.0 wRC: 47.894 wRC/PA: 0.177 wOBA: 0.383 BABIP: 0.294 WAR: 0.9 wRC+: 96.16579130136618
  ....
  Name: Eloy Jiménez PA: 0 wRC: -0.0 wRC/PA: 0.0 wOBA: 0.0 BABIP: 0.0 WAR: 0.0 wRC+: 0.0

  All batters currently on teams:
  Name: Jake Fraley PA: 83.0 wRC: 17.273 wRC/PA: 0.208 wOBA: 0.422 BABIP: 0.306 WAR: 0.3 wRC+: 100.44673175922586
  Name: Matt Olson PA: 267.0 wRC: 54.06 wRC/PA: 0.202 wOBA: 0.415 BABIP: 0.291 WAR: 0.9 wRC+: 99.82064713639215
  Name: Ramón Laureano PA: 210.0 wRC: 33.058 wRC/PA: 0.157 wOBA: 0.359 BABIP: 0.298 WAR: 0.7 wRC+: 99.71592739918019
  ....
  Name: Garrett Hampson PA: 241.0 wRC: 29.795 wRC/PA: 0.124 wOBA: 0.317 BABIP: 0.304 WAR: 0.8 wRC+: 79.39941787107149

  All free-agent batters:
  Name: Chad Pinder PA: 96.0 wRC: 12.873 wRC/PA: 0.134 wOBA: 0.33 BABIP: 0.339 WAR: 0.3 wRC+: 99.6995572763256
  Name: Mike Zunino PA: 162.0 wRC: 21.983 wRC/PA: 0.136 wOBA: 0.332 BABIP: 0.215 WAR: 0.5 wRC+: 99.65206371001915
  Name: Ty France PA: 254.0 wRC: 35.285 wRC/PA: 0.139 wOBA: 0.336 BABIP: 0.299 WAR: 0.8 wRC+: 99.630166860551
  ....
  Name: Derek Fisher PA: 2.0 wRC: -0.263 wRC/PA: -0.132 wOBA: 0.0 BABIP: 0.0 WAR: 0.0 wRC+: -5.554554043537899
