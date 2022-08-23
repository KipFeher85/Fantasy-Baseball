================================================
Yahoo Fantasy Baseball Statistic Analysis Module
================================================

Setup
-----
OAuth2.json setup

- Create an empty json file named 'OAuth2'
- Get access token and consumer key by register an app: https://developer.yahoo.com/apps/create/
- Place these within your OAuth2.json as done in this link: https://pypi.org/project/yahoo-oauth/

League Constants

- Make sure to call update_league_constants() ONCE AND ONLY ONCE PER DAY. This allows the user to run into less scenarios where they request too many times from a given API
- Make sure to call update_ballpark_constants ONCE per year. This only needs done once per season since it uses ballpark factors from the previous season
- Make sure to ALWAYS call starter() whenever using the package, it is required for ALL functions

Qualified Configurations

- Make sure to have your 'configs.yaml' file with the correct fields as shown on the GitHub project page

Multiple Leagues

- If you have multiple leagues simply pass in the league_id to the yfbsa.League object
- If "league_id" is not passed, it will default to the first league_id registered. The program will display a list of available id's however

Python Module Usage
-------------------

::

  In [1]: from yahoo_fb_stat_analysis import main as yfbsa

  In [2]: lgObj = yfbsa.League(year=2022)

  In [3]: lgObj.update_league_constants()

  In [4]: lgObj.update_ballpark_constants()

  In [5]: lgObj.starter()

  # Get Shane McClanahan's stats over the past month
  In [6]: shane = lgObj.get_player("Shane McClanahan", "lastmonth")
  Out[6]: {'Shane McClanahan': [11398.0, 5.0, 32.0, 122.0, 3.279, 31.967, 3.133, 1.41, 0.81, 39.0, 5.0, 3.0, 1.0, 0.0]}

  # Display Shane McClanahan's stats over the season
  In [7]: lgObj.print_player("Shane McClanahan", "season")
  Out[7]: Name: Shane McClanahan GS: 5.0 IP: 32.1 BF: 114.0 BB%: 3.509 K%: 36.842 FIP: 0.0 ERA: 1.39 WHIP: 0.65 W: 3.0 L: 0.0 SV: 0.0

  # Display your current roster's stats over the season
  In [8]: lgObj.current_roster_stats("season")
  Out[8]:
  Your batters:
  Current week:  11
  Current week roster:  [{'player_id': 11732, 'name': 'Adley Rutschman', 'status': '', 'position_type': 'B', 'eligible_positions': ['C', 'Util'], 'selected_position': 'C'}, {'player_id': 9605, 'name': 'Matt Olson', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', 'Util'], 'selected_position': '1B'}, {'player_id': 9112, 'name': 'Jurickson Profar', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', '2B', 'OF', 'Util'], 'selected_position': '2B'}, {'player_id': 11771, 'name': 'Bobby Witt Jr.', 'status': '', 'position_type': 'B', 'eligible_positions': ['3B', 'SS', 'Util'], 'selected_position': '3B'}, {'player_id': 10233, 'name': 'Amed Rosario', 'status': '', 'position_type': 'B', 'eligible_positions': ['SS', 'OF', 'Util'], 'selected_position': 'OF'}, {'player_id': 10429, 'name': 'Ryan Mountcastle', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', 'OF', 'Util'], 'selected_position': 'OF'}, {'player_id': 11391, 'name': 'Nolan Gorman', 'status': '', 'position_type': 'B', 'eligible_positions': ['2B', '3B', 'Util'], 'selected_position': 'Util'}, {'player_id': 9846, 'name': 'Christian Walker', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', 'Util'], 'selected_position': 'Util'}, {'player_id': 11370, 'name': 'Oneil Cruz', 'status': '', 'position_type': 'B', 'eligible_positions': ['SS', 'Util'], 'selected_position': 'BN'}, {'player_id': 9553, 'name': 'Albert Almora Jr.', 'status': '', 'position_type': 'B', 'eligible_positions': ['OF', 'Util'], 'selected_position': 'BN'}, {'player_id': 10883, 'name': 'Yordan Alvarez', 'status': '', 'position_type': 'B', 'eligible_positions': ['OF', 'Util'], 'selected_position': 'BN'}, {'player_id': 10839, 'name': 'Jazz Chisholm Jr.', 'status': '', 'position_type': 'B', 'eligible_positions': ['2B', 'SS', 'Util'], 'selected_position': 'BN'}, {'player_id': 11292, 'name': 'Jonathan India', 'status': 'DTD', 'position_type': 'B', 'eligible_positions': ['2B', 'Util'], 'selected_position': 'BN'}, {'player_id': 11398, 'name': 'Shane McClanahan', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'SP'}, {'player_id': 12281, 'name': 'Spencer Strider', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'RP', 'P'], 'selected_position': 'SP'}, {'player_id': 8287, 'name': 'David Robertson', 'status': '', 'position_type': 'P', 'eligible_positions': ['RP', 'P'], 'selected_position': 'RP'}, {'player_id': 10432, 'name': 'Tanner Scott', 'status': '', 'position_type': 'P', 'eligible_positions': ['RP', 'P'], 'selected_position': 'RP'}, {'player_id': 9620, 'name': 'Max Fried', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'P'}, {'player_id': 10462, 'name': 'Triston McKenzie', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'P'}, {'player_id': 11854, 'name': 'Alek Manoah', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'P'}, {'player_id': 11381, 'name': 'Logan Gilbert', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'P'}, {'player_id': 9121, 'name': 'Gerrit Cole', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'BN'}, {'player_id': 10940, 'name': 'MacKenzie Gore', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'BN'}, {'player_id': 10934, 'name': 'Shane Baz', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'BN'}, {'player_id': 10909, 'name': 'Trevor Rogers', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'BN'}, {'player_id': 10456, 'name': 'Tyler Stephenson', 'status': 'IL10', 'position_type': 'B', 'eligible_positions': ['C', '1B', 'Util', 'IL'], 'selected_position': 'IL'}, {'player_id': 10423, 'name': 'Mike Soroka', 'status': 'IL60', 'position_type': 'P', 'eligible_positions': ['SP', 'P', 'IL'], 'selected_position': 'IL'}, {'player_id': 11378, 'name': 'Esteury Ruiz', 'status': 'NA', 'position_type': 'B', 'eligible_positions': ['2B', 'Util', 'NA'], 'selected_position': 'NA'}]
  Name: Yordan Alvarez PA: 269.0 wRC: 60.804 wRC/PA: 0.226 wOBA: 0.443 BABIP: 0.301 WAR: 0.9 wRC+: 193.939
  Name: Brendan Donovan PA: 192.0 wRC: 33.219 wRC/PA: 0.173 wOBA: 0.378 BABIP: 0.386 WAR: 0.7 wRC+: 151.984
  ....

  Your pitchers:
  Name: Spencer Strider GS: 16.0 IP: 47.2 BF: 195.0 BB%: 11.282 K%: 36.923 FIP: 2.401 ERA: 3.4 WHIP: 1.11 WAR: 1.5 W: 3.0 L: 2.0 SV: 0.0
  Name: Max Fried GS: 15.0 IP: 94.1 BF: 376.0 BB%: 4.255 K%: 24.468 FIP: 2.611 ERA: 2.77 WHIP: 1.05 WAR: 3.3 W: 7.0 L: 2.0 SV: 0.0  ....
  ....

  # Get the basic info for all the players on your current roster
  In [9]: lgObj.current_roster_basic()
  Out[9]:
  Hitter List:
  {'player_id': 11732, 'name': 'Adley Rutschman', 'status': '', 'position_type': 'B', 'eligible_positions': ['C', 'Util'], 'selected_position': 'C'}
  {'player_id': 9605, 'name': 'Matt Olson', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', 'Util'], 'selected_position': '1B'}
  ....

  Pitcher List:
  {'player_id': 10432, 'name': 'Tanner Scott', 'status': '', 'position_type': 'P', 'eligible_positions': ['RP', 'P'], 'selected_position': 'RP'}
  {'player_id': 9620, 'name': 'Max Fried', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'P'}
  ....

  Injured List and NA:
  {'player_id': 11292, 'name': 'Jonathan India', 'status': 'DTD', 'position_type': 'B', 'eligible_positions': ['2B', 'Util'], 'selected_position': 'BN'}
  {'player_id': 10456, 'name': 'Tyler Stephenson', 'status': 'IL10', 'position_type': 'B', 'eligible_positions': ['C', '1B', 'Util', 'IL'], 'selected_position': 'IL'}
  ....

  # Get details for every team in your league
  In [10]: lgObj.team_details()
  Out[10]:
  [('team_key', 'team's key'), ('team_id', '10'), ('name', 'Name A'), ('url', 'team url'), ('team_logos', [{'team_logo': {'size': 'large', 'url': 'url'}}]), ('waiver_priority', 10), ('number_of_moves', '21'), ('number_of_trades', 0), ('roster_adds', {'coverage_type': 'week', 'coverage_value': 11, 'value': '1'}), ('league_scoring_type', 'head'), ('draft_position', 2), ('has_draft_grade', 0), ('managers', [{'manager': {'manager_id': '10', 'nickname': 'Mr. X', 'guid': 'B3QNT4MWWQDXZS3J7HDPCDPWVU', 'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg', 'felo_score': '658', 'felo_tier': 'silver'}}])]
  [('team_key', 'team's key'), ('team_id', '12'), ('name', 'Name B'), ('url', 'team url'), ('team_logos', [{'team_logo': {'size': 'large', 'url': 'url'}}]), ('waiver_priority', 12), ('number_of_moves', '16'), ('number_of_trades', 0), ('roster_adds', {'coverage_type': 'week', 'coverage_value': 11, 'value': '0'}), ('league_scoring_type', 'head'), ('draft_position', 3), ('has_draft_grade', 0), ('managers', [{'manager': {'manager_id': '12', 'nickname': 'Mr. Y', 'guid': 'JLUKFLTAHXRTWF46MW3YLFKE3E', 'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg', 'felo_score': '668', 'felo_tier': 'silver'}}])]
  ....

  # Display every game's matchup, pitcher stats over the past month, your batters stats over the past week, and a note if available
  In [11]: lgObj.predict_team_day()
  Out[11]:
  Game 1: New York Mets at Miami Marlins
  Pitcher Stats over the past month
  HP: Daniel Castano IP: 10.0 BF: 46.0 BB%: 10.87 K%: 13.043 FIP: 5.064 ERA: 3.6 WHIP: 1.7 K: 1.0 HR: 0.0
  AP: David Peterson IP: 20.1 BF: 97.0 BB%: 13.402 K%: 20.619 FIP: 4.358 ERA: 4.43 WHIP: 1.77 K: 1.0 HR: 2.0
  
  Game 2: Houston Astros at New York Yankees
  Pitcher Stats over the past month
  HP: Nestor Cortes IP: 10.0 BF: 46.0 BB%: 10.87 K%: 13.043 FIP: 5.064 ERA: 3.6 WHIP: 1.7 K: 1.0 HR: 0.0
  AP: Jose Urquidy IP: 27.0 BF: 125.0 BB%: 6.4 K%: 17.6 FIP: 5.423 ERA: 5.33 WHIP: 1.52 K: 6.0 HR: 2.0
  ....

  Team batter stats over the past week:
  Current week:  11
  Current week roster:  [{'player_id': 11732, 'name': 'Adley Rutschman', 'status': '', 'position_type': 'B', 'eligible_positions': ['C', 'Util'], 'selected_position': 'C'}, {'player_id': 9605, 'name': 'Matt Olson', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', 'Util'], 'selected_position': '1B'}, {'player_id': 9112, 'name': 'Jurickson Profar', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', '2B', 'OF', 'Util'], 'selected_position': '2B'}, {'player_id': 11771, 'name': 'Bobby Witt Jr.', 'status': '', 'position_type': 'B', 'eligible_positions': ['3B', 'SS', 'Util'], 'selected_position': '3B'}, {'player_id': 10233, 'name': 'Amed Rosario', 'status': '', 'position_type': 'B', 'eligible_positions': ['SS', 'OF', 'Util'], 'selected_position': 'OF'}, {'player_id': 10429, 'name': 'Ryan Mountcastle', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', 'OF', 'Util'], 'selected_position': 'OF'}, {'player_id': 11391, 'name': 'Nolan Gorman', 'status': '', 'position_type': 'B', 'eligible_positions': ['2B', '3B', 'Util'], 'selected_position': 'Util'}, {'player_id': 9846, 'name': 'Christian Walker', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', 'Util'], 'selected_position': 'Util'}, {'player_id': 11370, 'name': 'Oneil Cruz', 'status': '', 'position_type': 'B', 'eligible_positions': ['SS', 'Util'], 'selected_position': 'BN'}, {'player_id': 9553, 'name': 'Albert Almora Jr.', 'status': '', 'position_type': 'B', 'eligible_positions': ['OF', 'Util'], 'selected_position': 'BN'}, {'player_id': 10883, 'name': 'Yordan Alvarez', 'status': '', 'position_type': 'B', 'eligible_positions': ['OF', 'Util'], 'selected_position': 'BN'}, {'player_id': 10839, 'name': 'Jazz Chisholm Jr.', 'status': '', 'position_type': 'B', 'eligible_positions': ['2B', 'SS', 'Util'], 'selected_position': 'BN'}, {'player_id': 11292, 'name': 'Jonathan India', 'status': 'DTD', 'position_type': 'B', 'eligible_positions': ['2B', 'Util'], 'selected_position': 'BN'}, {'player_id': 11398, 'name': 'Shane McClanahan', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'SP'}, {'player_id': 12281, 'name': 'Spencer Strider', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'RP', 'P'], 'selected_position': 'SP'}, {'player_id': 8287, 'name': 'David Robertson', 'status': '', 'position_type': 'P', 'eligible_positions': ['RP', 'P'], 'selected_position': 'RP'}, {'player_id': 10432, 'name': 'Tanner Scott', 'status': '', 'position_type': 'P', 'eligible_positions': ['RP', 'P'], 'selected_position': 'RP'}, {'player_id': 9620, 'name': 'Max Fried', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'P'}, {'player_id': 10462, 'name': 'Triston McKenzie', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'P'}, {'player_id': 11854, 'name': 'Alek Manoah', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'P'}, {'player_id': 11381, 'name': 'Logan Gilbert', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'P'}, {'player_id': 9121, 'name': 'Gerrit Cole', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'BN'}, {'player_id': 10940, 'name': 'MacKenzie Gore', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'BN'}, {'player_id': 10934, 'name': 'Shane Baz', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'BN'}, {'player_id': 10909, 'name': 'Trevor Rogers', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'BN'}, {'player_id': 10456, 'name': 'Tyler Stephenson', 'status': 'IL10', 'position_type': 'B', 'eligible_positions': ['C', '1B', 'Util', 'IL'], 'selected_position': 'IL'}, {'player_id': 10423, 'name': 'Mike Soroka', 'status': 'IL60', 'position_type': 'P', 'eligible_positions': ['SP', 'P', 'IL'], 'selected_position': 'IL'}, {'player_id': 11378, 'name': 'Esteury Ruiz', 'status': 'NA', 'position_type': 'B', 'eligible_positions': ['2B', 'Util', 'NA'], 'selected_position': 'NA'}]
  Name: Jazz Chisholm Jr. PA: 24.0 wRC: 7.226 wRC/PA: 0.301 wOBA: 0.535 BABIP: 0.538 wRC+: 222.084
  Name: Yordan Alvarez PA: 21.0 wRC: 6.357 wRC/PA: 0.303 wOBA: 0.537 BABIP: 0.222 wRC+: 220.66
  ....

  Team pitcher stats over the past week:
  Name: Max Fried GS: 2.0 IP: 13.2 BF: 52.0 BB%: 5.769 K%: 32.692 FIP: 1.270 ERA: 1.98 WHIP: 1.02 W: 0.0 L: 0.0 SV: 0.0
  Name: Triston McKenzie GS: 1.0 IP: 4.1 BF: 22.0 BB%: 4.545 K%: 22.727 FIP: 10.969 ERA: 12.46 WHIP: 2.31 W: 0.0 L: 0.0 SV: 0.0
  ....

  # Get a dict of all the batters currently on the wire with their stats over the past month only considering qualified batters
  In [12]: faBatters = lgObj.get_batters('lastmonth', status=2, qualified=True)
  Out[12]: {'Albert Pujols': [63.0, 5.0, 16.667, 0.267, 0.283, 0.884, 0.376, 10.779, 0.0, 97.580, 0.171] .... }

  # Display all qualified batters currently on the wire with their stats over the past month
  In [13]: lgObj.print_batters(faBatters, reverse=True)
  Out[13]:
  Name: Luis Torrens PA: 9.0 wRC: 3.835 wRC/PA: 0.426 wOBA: 0.693 BABIP: 0.333 wRC+: 127.428
  Name: Luis Rengifo PA: 4.0 wRC: 0.897 wRC/PA: 0.224 wOBA: 0.442 BABIP: 0.667 wRC+: 118.299
  ....

  # Get a dict of all the pitchers currently on the wire with their stats over the past month only considering qualified pitchers
  In [14]: takenPitchers = lgObj.get_pitchers('lastmonth', status=1, qualified=True)
  Out[14]: {'Adam Wainwright': [7048, 8.0, 32.0, 131.0, '9.160', '24.427', '3.102', 2.53, 1.19, 32.0, 2.0, 3.0, 0.0, 0.0], ....}

  # Display all qualified pitchers currently on the wire with their stats over the past month
  In [15]: lgObj.print_pitchers(takenPitchers, reverse=False)
  Out[15]:
  Name: Ryan Pressly GS: 12.0 IP: 12.0 BF: 40.0 BB%: 0.000 K%: 52.500 FIP: -0.336 ERA: 0.0 WHIP: 0.33 W: 2.0 L: 0.0 SV: 6.0
  Name: Paul Sewald GS: 13.0 IP: 12.2 BF: 45.0 BB%: 6.667 K%: 48.889 FIP: 0.295 ERA: 0.0 WHIP: 0.47 W: 3.0 L: 0.0 SV: 2.0

  # Display whether a player is currently over-achieving or under-achieving
  In [16]: lgObj.outlier("Shane McClanahan", 1)
  Out[16]:
  Current Season Stats
  Name: Shane McClanahan GS: 14.0 IP: 84.1 BF: 320.0 BB%: 5.0 K%: 35.312 FIP: 2.784 ERA: 1.81 WHIP: 0.85 WAR: 2.2 W: 7.0 L: 3.0 SV: 0.0
  Career Stats
  Name: Shane McClanahan GS: 40.0 IP: 211.2 BF: 794.0 BB%: 6.675 K%: 32.746 FIP: 3.036 ERA: 2.76 WHIP: 1.1 W: 17.0 L: 9.0 SV: 0.0
  Up 0.252 points in FIP
  Up 0.950 points in ERA
  Up 0.250 points in WHIP
  Up 2.566 points in K%
  Up 1.675 points in BB%
  Currently overachieving based on the following categories:
  FIP, ERA, WHIP, K%, BB%

  # Display the top 10 hottest batter and pitchers both rostered and on the wire over the season
  # Batters sorted by wRC+ descending
  # Pitchers sorted by FIP ascending
  In [17]: lgObj.whos_hot("season")
  Out[17]:
  Top 10 Hottest Rostered Pitchers:
  Name: Jason Adam GS: 32.0 IP: 29.2 BF: 107.0 BB%: 7.477 K%: 29.907 FIP: 2.000 ERA: 1.21 WHIP: 0.67 WAR: 0.8 W: 1.0 L: 2.0 SV: 2.0
  Name: Seranthony Domínguez GS: 29.0 IP: 27.2 BF: 104.0 BB%: 6.731 K%: 33.654 FIP: 1.951 ERA: 1.63 WHIP: 0.83 WAR: 0.8 W: 4.0 L: 1.0 SV: 2.0
  ....

  Top 10 Hottest Free Agent Pitchers:
  Name: Cody Stashak GS: 11.0 IP: 16.1 BF: 65.0 BB%: 0.000 K%: 23.077 FIP: 2.108 ERA: 3.86 WHIP: 0.98 WAR: 0.4 W: 3.0 L: 0.0 SV: 0.0
  Name: Daniel Hudson GS: 25.0 IP: 24.1 BF: 97.0 BB%: 5.155 K%: 30.928 FIP: 2.085 ERA: 2.22 WHIP: 0.9 WAR: 0.7 W: 2.0 L: 3.0 SV: 5.0
  ....

  Top 10 Hottest Rostered Batters:
  Name: Paul Goldschmidt PA: 308.0 wRC: 69.117 wRC/PA: 0.224 wOBA: 0.441 BABIP: 0.382 WAR: 1.1 wRC+: 195.611
  Name: Yordan Alvarez PA: 269.0 wRC: 60.804 wRC/PA: 0.226 wOBA: 0.443 BABIP: 0.301 WAR: 0.9 wRC+: 193.939
  ....

  Top 10 Hottest Free Agent Batters:
  Name: Ji-Man Choi PA: 194.0 wRC: 32.774 wRC/PA: 0.169 wOBA: 0.373 BABIP: 0.383 WAR: 0.7 wRC+: 143.655
  Name: Luis González PA: 180.0 wRC: 26.885 wRC/PA: 0.149 wOBA: 0.349 BABIP: 0.366 WAR: 0.6 wRC+: 130.883
  ....

  # Display the top 10 coldest batter and pitchers both rostered and on the wire over the season
  # Batters sorted by wRC+ ascending
  # Pitchers sorted by FIP descending
  In [18]: lgObj.whos_cold("season")
  Out[18]:
  Top 10 Coldest Rostered Pitchers:
  Name: Hunter Greene GS: 14.0 IP: 70.0 BF: 305.0 BB%: 9.836 K%: 28.852 FIP: 5.735 ERA: 5.66 WHIP: 1.36 WAR: 0.0 W: 3.0 L: 8.0 SV: 0.0
  Name: Beau Brieske GS: 11.0 IP: 59.2 BF: 247.0 BB%: 6.883 K%: 16.599 FIP: 5.495 ERA: 4.07 WHIP: 1.21 WAR: -0.3 W: 1.0 L: 6.0 SV: 0.0
  ....

  Top 10 Coldest Free Agent Pitchers:
  Name: Albert Abreu GS: 12.0 IP: 14.0 BF: 68.0 BB%: 25.000 K%: 17.647 FIP: 8.307 ERA: 3.21 WHIP: 2.0 WAR: -0.1 W: 0.0 L: 0.0 SV: 0.0
  Name: Trevor Kelley GS: 13.0 IP: 16.0 BF: 72.0 BB%: 5.556 K%: 20.833 FIP: 8.101 ERA: 7.31 WHIP: 1.38 WAR: -0.6 W: 1.0 L: 0.0 SV: 0.0
  ....

  Top 10 Coldest Rostered Batters:
  Name: Elias Díaz PA: 177.0 wRC: 14.743 wRC/PA: 0.083 wOBA: 0.268 BABIP: 0.248 WAR: 0.6 wRC+: 57.472
  Name: Jorge Mateo PA: 239.0 wRC: 17.568 wRC/PA: 0.074 wOBA: 0.256 BABIP: 0.284 WAR: 0.8 wRC+: 58.391
  ....

  Top 10 Coldest Free Agent Batters:
  Name: Pat Valaika PA: 163.0 wRC: 8.791 wRC/PA: 0.054 wOBA: 0.232 BABIP: 0.269 WAR: 0.5 wRC+: 44.287
  Name: Kevin Newman PA: 319.0 wRC: 17.985 wRC/PA: 0.056 wOBA: 0.235 BABIP: 0.217 WAR: 1.0 wRC+: 48.883
  ....

  In [19]: lgObj.get_all_players('lastmonth', qualified=True)
  Out[19]:
  All pitchers currently on your team:
  Name: Chad Green GS: 9.0 IP: 13.2 BF: 50.0 BB%: 0.000 K%: 38.000 FIP: 1.270 ERA: 3.29 WHIP: 0.66 W: 3.0 L: 1.0 SV: 1.0
  Name: Zach Thompson GS: 3.0 IP: 16.0 BF: 64.0 BB%: 9.375 K%: 37.500 FIP: 2.477 ERA: 2.25 WHIP: 0.94 W: 1.0 L: 1.0 SV: 0.0
  ....

  All batters currently on your team:
  Name: Kyle Schwarber PA: 77.0 wRC: 23.748 wRC/PA: 0.308 wOBA: 0.544 BABIP: 0.303 wRC+: 246.399
  Name: Max Muncy PA: 75.0 wRC: 16.708 wRC/PA: 0.223 wOBA: 0.439 BABIP: 0.255 wRC+: 184.203
  ....

  All pitchers currently on teams:
  Name: Ryan Pressly GS: 12.0 IP: 12.0 BF: 40.0 BB%: 0.000 K%: 52.500 FIP: -0.336 ERA: 0.0 WHIP: 0.33 W: 2.0 L: 0.0 SV: 6.0
  Name: Paul Sewald GS: 13.0 IP: 12.2 BF: 45.0 BB%: 6.667 K%: 48.889 FIP: 0.295 ERA: 0.0 WHIP: 0.47 W: 3.0 L: 0.0 SV: 2.0
  ....

  All batters currently on teams:
  Name: Kyle Schwarber PA: 77.0 wRC: 23.748 wRC/PA: 0.308 wOBA: 0.544 BABIP: 0.303 wRC+: 246.399
  Name: Joey Gallo PA: 93.0 wRC: 28.759 wRC/PA: 0.309 wOBA: 0.545 BABIP: 0.258 wRC+: 242.521
  ....

  All free-agent pitchers
  Name: Collin McHugh GS: 6.0 IP: 14.1 BF: 46.0 BB%: 0.000 K%: 39.130 FIP: 0.611 ERA: 0.0 WHIP: 0.35 W: 1.0 L: 0.0 SV: 0.0
  Name: Jesse Chávez GS: 5.0 IP: 7.2 BF: 28.0 BB%: 7.143 K%: 42.857 FIP: 0.664 ERA: 2.35 WHIP: 0.65 W: 0.0 L: 1.0 SV: 0.0
  ....

  All free-agent batters:
  Name: Curt Casali PA: 45.0 wRC: 16.375 wRC/PA: 0.364 wOBA: 0.612 BABIP: 0.565 wRC+: 295.889
  Name: Garrett Cooper PA: 54.0 wRC: 18.372 wRC/PA: 0.34 wOBA: 0.583 BABIP: 0.6 wRC+: 278.776
  ....
