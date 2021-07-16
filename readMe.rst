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

- Make sure to call update_league_constats() ONCE AND ONLY ONCE PER DAY. This allows the user to run into less scenarios where they request too many times from a given API
- Make sure to allways call starter() whenever using the package, it is required for all functions

Python Module Usage
-------------------

::

  In [1]: from yahoo_oauth import OAuth2

  In [2]: import yahoo_fantasy_api as yfa

  In [3]: import json

  In [4]: import csv

  In [5]: import pandas as pd

  In [6]: from datetime import date

  In [7]: from dateutil.relativedelta import relativedelta

  In [8]: from yahoo_fb_stat_analysis import main as yfbsa

  In [9]: lgObj = League()

  In [10]: lgObj.update_league_constants()

  In [11]: lgObj.starter()

  In [12]: trey = lgObj.get_player("Trey Mancini", "season")
  Out[12]: {'Trey Mancini': [362.0, 9.877, 25.926, 0.298, 0.256, 0.791, 0.344, 52.593, 1.2, 119.304, 0.145]}

  In [13]: lgObj.print_player("Trey Mancini", "season")
  Out[13]: Name: Trey Mancini PA: 362.0 wRC: 52.593 wRC/PA: 0.145 wOBA: 0.344 BABIP: 0.298 WAR: 1.2 wRC+: 119.304

  In [14]: lgObj.current_roster_stats("season")
  Out[14]:
  Your batters:
  Name: Max Muncy PA: 319.0 wRC: 66.641 wRC/PA: 0.209 wOBA: 0.422 BABIP: 0.278 WAR: 1.0 wRC+: 182.453
  Name: Brandon Crawford PA: 302.0 wRC: 56.193 wRC/PA: 0.186 wOBA: 0.394 BABIP: 0.316 WAR: 1.0 wRC+: 161.026
  ....
  Name: Vidal Bruján PA: 9.0 wRC: -0.498 wRC/PA: -0.055 wOBA: 0.098 BABIP: 0.167 WAR: 0.0 wRC+: -41.524

  Your pitchers:
  Name: Zach Thompson GS: 5.0 IP: 24.0 BF: 97.0 BB%: 7.216 K%: 31.959 FIP: 2.247 ERA: 2.25 WHIP: 1.0 WAR: 0.9 W: 2.0 L: 2.0 SV: 0.0
  Name: Anthony Bender GS: 28.0 IP: 29.1 BF: 110.0 BB%: 6.364 K%: 35.455 FIP: 2.408 ERA: 1.84 WHIP: 0.78 WAR: 0.7 W: 1.0 L: 0.0 SV: 1.0
  ....
  Name: Triston McKenzie GS: 12.0 IP: 49.1 BF: 212.0 BB%: 18.868 K%: 32.075 FIP: 4.956 ERA: 5.47 WHIP: 1.4 WAR: 0.3 W: 1.0 L: 3.0 SV: 0.0

  In [15]: lgObj.current_roster_basic()
  Out[15]:
  Hitter List:
  {'player_id': 9718, 'name': 'J.T. Realmuto', 'status': '', 'position_type': 'B', 'eligible_positions': ['C', 'Util'], 'selected_position': 'C'}
  {'player_id': 9606, 'name': 'Max Muncy', 'status': '', 'position_type': 'B', 'eligible_positions': ['1B', '2B', '3B', 'Util'], 'selected_position': '1B'}
  ....
  {'player_id': 9345, 'name': 'Leury García', 'status': '', 'position_type': 'B', 'eligible_positions': ['2B', '3B', 'SS', 'OF', 'Util'], 'selected_position': 'BN'}

  Pitcher List:
  {'player_id': 11854, 'name': 'Alek Manoah', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'SP'}
  {'player_id': 11253, 'name': 'Jordan Romano', 'status': '', 'position_type': 'P', 'eligible_positions': ['RP', 'P'], 'selected_position': 'RP'}
  ....
  {'player_id': 11903, 'name': 'Luis Garcia', 'status': '', 'position_type': 'P', 'eligible_positions': ['SP', 'P'], 'selected_position': 'BN'}

  Injured List and NA:
  {'player_id': 10439, 'name': 'Eloy Jiménez', 'status': 'IL60', 'position_type': 'B', 'eligible_positions': ['OF', 'Util', 'IL'], 'selected_position': 'IL'}
  {'player_id': 9861, 'name': 'Kyle Schwarber', 'status': 'IL10', 'position_type': 'B', 'eligible_positions': ['OF', 'Util', 'IL'], 'selected_position': 'IL'}
  ....
  {'player_id': 12202, 'name': 'Zach Thompson', 'status': 'DTD', 'position_type': 'P', 'eligible_positions': ['SP', 'RP', 'P'], 'selected_position': 'SP'}

  In [16]: lgObj.teamDetails()
  Out[16]:
  [('team_key', 'team's key'), ('team_id', '10'), ('name', 'Name A'), ('url', 'team url'), ('team_logos', [{'team_logo': {'size': 'large', 'url': 'url'}}]), ('waiver_priority', 10), ('number_of_moves', '21'), ('number_of_trades', 0), ('roster_adds', {'coverage_type': 'week', 'coverage_value': 11, 'value': '1'}), ('league_scoring_type', 'head'), ('draft_position', 2), ('has_draft_grade', 0), ('managers', [{'manager': {'manager_id': '10', 'nickname': 'Mr. X', 'guid': 'B3QNT4MWWQDXZS3J7HDPCDPWVU', 'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg', 'felo_score': '658', 'felo_tier': 'silver'}}])]
  [('team_key', 'team's key'), ('team_id', '12'), ('name', 'Name B'), ('url', 'team url'), ('team_logos', [{'team_logo': {'size': 'large', 'url': 'url'}}]), ('waiver_priority', 12), ('number_of_moves', '16'), ('number_of_trades', 0), ('roster_adds', {'coverage_type': 'week', 'coverage_value': 11, 'value': '0'}), ('league_scoring_type', 'head'), ('draft_position', 3), ('has_draft_grade', 0), ('managers', [{'manager': {'manager_id': '12', 'nickname': 'Mr. Y', 'guid': 'JLUKFLTAHXRTWF46MW3YLFKE3E', 'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg', 'felo_score': '668', 'felo_tier': 'silver'}}])]
  ....
  [('team_key', 'team's key'), ('team_id', '2'), ('name', 'Name C'), ('url', 'team url'), ('team_logos', [{'team_logo': {'size': 'large', 'url': 'url'}}]), ('waiver_priority', 1), ('number_of_moves', '1'), ('number_of_trades', 0), ('roster_adds', {'coverage_type': 'week', 'coverage_value': 11, 'value': '0'}), ('league_scoring_type', 'head'), ('draft_position', 12), ('has_draft_grade', 0), ('managers', [{'manager': {'manager_id': '2', 'nickname': 'Mr. Z', 'guid': '7NIG4ZRBEELFHB43MOYUGCW3KU', 'image_url': 'https://s.yimg.com/ag/images/default_user_profile_pic_64sq.jpg', 'felo_score': '477', 'felo_tier': 'bronze'}}])]

  In [17]: lgObj.predictTeamDay()
  Out[17]:
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
  Game 3: Houston Astros at Baltimore Orioles
  Pitcher Stats over the past month
  HP: Keegan Akin IP: 23.1 BF: 106.0 BB%: 12.26 K%: 20.75 FIP: 5.17 ERA: 6.56 WHIP: 1.71 K: 22.0 HR: 4.0
  Keegan Akin Note: Akin endured a strange start his last time out, allowing eight runs while stiking out seven over 5 2/3 innings against Cleveland. The rookie lefty pitched to a 2.63 ERA over his first three starts.
  AP: Jake Odorizzi IP: 22.1 BF: 84.0 BB%: 7.14 K%: 28.57 FIP: 2.95 ERA: 2.82 WHIP: 0.81 K: 24.0 HR: 2.0
  Jake Odorizzi Note: Jake Odorizzi opens the series at Camden Yards for the Astros. The right-hander is 3-3 with a 4.83 ERA in 10 career starts in Baltimore.

  Game 4: Cleveland Indians at Chicago Cubs
  Pitcher Stats over the past month
  HP: Adbert Alzolay IP: 18.1 BF: 82.0 BB%: 12.2 K%: 26.83 FIP: 4.68 ERA: 3.93 WHIP: 1.42 K: 22.0 HR: 3.0
  Adbert Alzolay Note: Alzolay is expected to be activated from the 10-day IL after dealing with a blister on his right middle finger. In the seven starts prior to the blister-impacted game on June 7, the righty had 41 strikeouts vs. six walks with a 2.95 ERA in 39 2/3 innings.
  AP: Aaron Civale IP: 29.2 BF: 119.0 BB%: 5.04 K%: 19.33 FIP: 4.95 ERA: 3.94 WHIP: 1.21 K: 23.0 HR: 6.0
  Aaron Civale Note: With Shane Bieber and Zach Plesac on the IL, Civale is the front man of the Indians' rotation. He will take the mound against the Cubs for the second time in his career. Civale's previous start vs. Chicago saw him allow just two runs over six innings.

  ....
  Game 8: Los Angeles Dodgers at San Diego Padres
  Pitcher Stats over the past month
  HP: Yu Darvish IP: 28.1 BF: 113.0 BB%: 7.96 K%: 30.09 FIP: 4.2 ERA: 4.13 WHIP: 0.99 K: 34.0 HR: 5.0
  Yu Darvish Note: The Padres won 11 of Darvish's first 12 starts, but they've now lost two straight. Still, Darvish was mostly sharp in those two outings. He's allowed just 59 hits while striking out 97 across 84 innings this season.
  AP: Julio Urias IP: 25.2 BF: 117.0 BB%: 8.55 K%: 21.37 FIP: 5.43 ERA: 6.31 WHIP: 1.68 K: 25.0 HR: 6.0
  Julio Urias Note: Urías has made eight career appearances (three starts) against San Diego, going 1-0 with a 2.08 ERA. This will be his first start against the Padres this season.

  Team batter stats over the past week:
  Name: Leury García PA: 20.0 wRC: 6.168 wRC/PA: 0.308 wOBA: 0.544 BABIP: 0.538 wRC+: 268.947
  Name: Paul Goldschmidt PA: 14.0 wRC: 4.638 wRC/PA: 0.331 wOBA: 0.572 BABIP: 0.444 wRC+: 243.042
  ....
  Name: Vidal Bruján PA: 9.0 wRC: -0.498 wRC/PA: -0.055 wOBA: 0.098 BABIP: 0.167 wRC+: -43.925

  Team pitcher stats over the past week:
  Name: Heath Hembree GS: 3.0 IP: 3.0 BF: 10.0 BB%: 10.000 K%: 50.000 FIP: 0.831 ERA: 0.0 WHIP: 0.33 W: 0.0 L: 0.0 SV: 3.0
  Name: Triston McKenzie GS: 1.0 IP: 7.0 BF: 23.0 BB%: 4.348 K%: 39.130 FIP: 1.021 ERA: 0.0 WHIP: 0.29 W: 0.0 L: 0.0 SV: 0.0
  ....
  Name: Max Scherzer GS: 1.0 IP: 3.2 BF: 19.0 BB%: 5.263 K%: 36.842 FIP: 9.726 ERA: 17.18 WHIP: 1.64 W: 0.0 L: 0.0 SV: 0.0

  In [18]: faBatters = lgObj.get_batters('lastmonth', status=2, qualified=True)
  Out[18]: {'Albert Pujols': [63.0, 5.0, 16.667, 0.267, 0.283, 0.884, 0.376, 10.779, 0.0, 97.580, 0.171] .... }

  In [19]: lgObj.print_batters(faBatters, reverse=True)
  Out[19]:
  Name: Luis Torrens PA: 9.0 wRC: 3.835 wRC/PA: 0.426 wOBA: 0.693 BABIP: 0.333 wRC+: 127.428
  Name: Luis Rengifo PA: 4.0 wRC: 0.897 wRC/PA: 0.224 wOBA: 0.442 BABIP: 0.667 wRC+: 118.299
  ....
  Name: Derek Fisher PA: 2.0 wRC: -0.263 wRC/PA: -0.132 wOBA: 0.0 BABIP: 0.0 wRC+: -5.55

  In [20]: takenPitchers = lgObj.get_pitchers('lastmonth', status=1, qualified=True)
  Out[20]: {'Adam Wainwright': [7048, 8.0, 32.0, 131.0, '9.160', '24.427', '3.102', 2.53, 1.19, 32.0, 2.0, 3.0, 0.0, 0.0], ....}

  In [21]: lgObj.print_pitchers(takenPitchers, reverse=False)
  Out[21]:
  Name: Ryan Pressly GS: 12.0 IP: 12.0 BF: 40.0 BB%: 0.000 K%: 52.500 FIP: -0.336 ERA: 0.0 WHIP: 0.33 W: 2.0 L: 0.0 SV: 6.0
  Name: Paul Sewald GS: 13.0 IP: 12.2 BF: 45.0 BB%: 6.667 K%: 48.889 FIP: 0.295 ERA: 0.0 WHIP: 0.47 W: 3.0 L: 0.0 SV: 2.0
  ....
  Name: Adbert Alzolay GS: 4.0 IP: 19.2 BF: 83.0 BB%: 7.229 K%: 22.892 FIP: 7.695 ERA: 6.41 WHIP: 1.22 W: 0.0 L: 4.0 SV: 0.0

  In [22]: lgObj.outlier("Jacob deGrom", 1)
  Out[22]:
  Name: Jacob deGrom GS: 15.0 IP: 92.0 BF: 324.0 BB%: 3.395 K%: 45.062 FIP: 1.229 ERA: 1.08 WHIP: 0.54 WAR: 4.6 W: 7.0 L: 2.0 SV: 0.0
  Name: Jacob deGrom GS: 198.0 IP: 1261.2 BF: 4601.0 BB%: 6.412 K%: 32.71 FIP: 2.642 ERA: 2.5 WHIP: 1.01 W: 77.0 L: 53.0 SV: 0.0
  Up 1.413 points in FIP
  Up 1.420 points in ERA
  Up 0.470 points in WHIP
  Up 12.352 points in K%
  Up 3.017 points in BB%
  Currently overachieving based on the following categories:
  FIP, ERA, WHIP, K%, BB%

  In [23]: lgObj.whos_hot("season")
  Out[23]:
  Top 10 Hottest Rostered Pitchers:
  Name: Paul Sewald GS: 25.0 IP: 25.2 BF: 103.0 BB%: 10.680 K%: 42.718 FIP: 0.981 ERA: 1.4 WHIP: 0.94 WAR: 1.0 W: 5.0 L: 2.0 SV: 2.0
  Name: Craig Kimbrel GS: 33.0 IP: 31.2 BF: 117.0 BB%: 8.547 K%: 46.154 FIP: 1.081 ERA: 0.57 WHIP: 0.66 WAR: 1.2 W: 1.0 L: 2.0 SV: 20.0
  ....
  Name: Zach Thompson GS: 5.0 IP: 24.0 BF: 97.0 BB%: 7.216 K%: 31.959 FIP: 2.247 ERA: 2.25 WHIP: 1.0 WAR: 0.9 W: 2.0 L: 2.0 SV: 0.0

  Top 10 Hottest Free Agent Pitchers:
  Name: Collin McHugh GS: 21.0 IP: 37.2 BF: 143.0 BB%: 4.895 K%: 37.762 FIP: 1.255 ERA: 1.67 WHIP: 0.9 WAR: 1.5 W: 2.0 L: 1.0 SV: 0.0
  Name: Aaron Loup GS: 31.0 IP: 28.0 BF: 111.0 BB%: 5.405 K%: 30.631 FIP: 1.485 ERA: 1.61 WHIP: 1.0 WAR: 0.9 W: 3.0 L: 0.0 SV: 0.0
  ....
  Name: Scott Barlow GS: 41.0 IP: 42.2 BF: 184.0 BB%: 10.326 K%: 32.609 FIP: 2.429 ERA: 2.95 WHIP: 1.29 WAR: 1.1 W: 2.0 L: 3.0 SV: 4.0

  Top 10 Hottest Rostered Batters:
  Name: Vladimir Guerrero Jr. PA: 374.0 wRC: 90.639 wRC/PA: 0.242 wOBA: 0.463 BABIP: 0.344 WAR: 1.2 wRC+: 196.053
  Name: Fernando Tatis Jr. PA: 313.0 wRC: 66.92 wRC/PA: 0.214 wOBA: 0.428 BABIP: 0.311 WAR: 1.0 wRC+: 184.571
  ....
  Name: Xander Bogaerts PA: 361.0 wRC: 68.349 wRC/PA: 0.189 wOBA: 0.398 BABIP: 0.361 WAR: 1.2 wRC+: 151.531

  Top 10 Hottest Free Agent Batters:
  Name: Ronald Acuña Jr. PA: 360.0 wRC: 74.326 wRC/PA: 0.206 wOBA: 0.419 BABIP: 0.311 WAR: 1.2 wRC+: 174.263
  Name: Garrett Cooper PA: 238.0 wRC: 41.178 wRC/PA: 0.173 wOBA: 0.378 BABIP: 0.383 WAR: 0.8 wRC+: 151.984
  ....
  Name: Harold Ramirez PA: 200.0 wRC: 28.241 wRC/PA: 0.141 wOBA: 0.339 BABIP: 0.303 WAR: 0.6 wRC+: 112.999

  In [24]: lgObj.whos_cold("season")
  Out[24]:

  Top 10 Coldest Rostered Pitchers:
  Name: Marco Gonzales GS: 11.0 IP: 56.2 BF: 247.0 BB%: 8.502 K%: 19.838 FIP: 6.118 ERA: 5.88 WHIP: 1.46 WAR: -0.3 W: 1.0 L: 5.0 SV: 0.0
  Name: Stephen Strasburg GS: 5.0 IP: 21.2 BF: 95.0 BB%: 14.737 K%: 22.105 FIP: 5.758 ERA: 4.57 WHIP: 1.38 WAR: 0.0 W: 1.0 L: 2.0 SV: 0.0
  ....
  Name: Kyle Hendricks GS: 18.0 IP: 105.0 BF: 445.0 BB%: 4.494 K%: 17.978 FIP: 4.831 ERA: 3.77 WHIP: 1.25 WAR: 0.5 W: 11.0 L: 4.0 SV: 0.0

  Top 10 Coldest Free Agent Pitchers:
  Name: Jerad Eickhoff GS: 4.0 IP: 12.2 BF: 58.0 BB%: 6.897 K%: 10.345 FIP: 9.557 ERA: 4.97 WHIP: 1.66 WAR: -0.5 W: 0.0 L: 1.0 SV: 0.0
  Name: Seth Frankoff GS: 4.0 IP: 14.2 BF: 74.0 BB%: 12.162 K%: 14.865 FIP: 7.601 ERA: 9.2 WHIP: 1.98 WAR: -0.2 W: 0.0 L: 2.0 SV: 0.0
  ....
  Name: Cionel Pérez GS: 22.0 IP: 20.0 BF: 96.0 BB%: 19.792 K%: 19.792 FIP: 6.714 ERA: 7.2 WHIP: 1.9 WAR: -0.4 W: 1.0 L: 2.0 SV: 0.0

  Top 10 Coldest Rostered Batters:
  Name: Hunter Dozier PA: 277.0 wRC: 20.362 wRC/PA: 0.074 wOBA: 0.256 BABIP: 0.22 WAR: 0.9 wRC+: 58.391
  Name: Martín Maldonado PA: 239.0 wRC: 16.009 wRC/PA: 0.067 wOBA: 0.248 BABIP: 0.231 WAR: 0.8 wRC+: 60.942
  ....
  Name: Jon Berti PA: 249.0 wRC: 25.006 wRC/PA: 0.1 wOBA: 0.289 BABIP: 0.27 WAR: 0.8 wRC+: 90.353

  Top 10 Coldest Free Agent Batters:
  Name: Pat Valaika PA: 163.0 wRC: 8.791 wRC/PA: 0.054 wOBA: 0.232 BABIP: 0.269 WAR: 0.5 wRC+: 44.287
  Name: Kevin Newman PA: 319.0 wRC: 17.985 wRC/PA: 0.056 wOBA: 0.235 BABIP: 0.217 WAR: 1.0 wRC+: 48.883
  ....
  Name: Jorge Alfaro PA: 159.0 wRC: 11.817 wRC/PA: 0.074 wOBA: 0.257 BABIP: 0.312 WAR: 0.5 wRC+: 68.193

  In [25]: lgObj.getAllPlayers('lastmonth')
  Out[25]:
  All pitchers currently on your team:
  Name: Chad Green GS: 9.0 IP: 13.2 BF: 50.0 BB%: 0.000 K%: 38.000 FIP: 1.270 ERA: 3.29 WHIP: 0.66 W: 3.0 L: 1.0 SV: 1.0
  Name: Zach Thompson GS: 3.0 IP: 16.0 BF: 64.0 BB%: 9.375 K%: 37.500 FIP: 2.477 ERA: 2.25 WHIP: 0.94 W: 1.0 L: 1.0 SV: 0.0
  ....
  Name: Max Scherzer GS: 4.0 IP: 20.2 BF: 88.0 BB%: 7.955 K%: 34.091 FIP: 4.253 ERA: 4.35 WHIP: 1.11 W: 2.0 L: 0.0 SV: 0.0

  All batters currently on your team:
  Name: Kyle Schwarber PA: 77.0 wRC: 23.748 wRC/PA: 0.308 wOBA: 0.544 BABIP: 0.303 wRC+: 246.399
  Name: Max Muncy PA: 75.0 wRC: 16.708 wRC/PA: 0.223 wOBA: 0.439 BABIP: 0.255 wRC+: 184.203
  ....
  Name: Trey Mancini PA: 99.0 wRC: 10.265 wRC/PA: 0.104 wOBA: 0.293 BABIP: 0.271 wRC+: 81.318

  All pitchers currently on teams:
  Name: Ryan Pressly GS: 12.0 IP: 12.0 BF: 40.0 BB%: 0.000 K%: 52.500 FIP: -0.336 ERA: 0.0 WHIP: 0.33 W: 2.0 L: 0.0 SV: 6.0
  Name: Paul Sewald GS: 13.0 IP: 12.2 BF: 45.0 BB%: 6.667 K%: 48.889 FIP: 0.295 ERA: 0.0 WHIP: 0.47 W: 3.0 L: 0.0 SV: 2.0
  ....
  Name: Adbert Alzolay GS: 4.0 IP: 19.2 BF: 83.0 BB%: 7.229 K%: 22.892 FIP: 7.695 ERA: 6.41 WHIP: 1.22 W: 0.0 L: 4.0 SV: 0.0

  All batters currently on teams:
  Name: Kyle Schwarber PA: 77.0 wRC: 23.748 wRC/PA: 0.308 wOBA: 0.544 BABIP: 0.303 wRC+: 246.399
  Name: Joey Gallo PA: 93.0 wRC: 28.759 wRC/PA: 0.309 wOBA: 0.545 BABIP: 0.258 wRC+: 242.521
  ....
  Name: Ryan Zimmerman PA: 41.0 wRC: 0.272 wRC/PA: 0.007 wOBA: 0.174 BABIP: 0.172 wRC+: 3.4

  All free-agent pitchers
  Name: Collin McHugh GS: 6.0 IP: 14.1 BF: 46.0 BB%: 0.000 K%: 39.130 FIP: 0.611 ERA: 0.0 WHIP: 0.35 W: 1.0 L: 0.0 SV: 0.0
  Name: Jesse Chávez GS: 5.0 IP: 7.2 BF: 28.0 BB%: 7.143 K%: 42.857 FIP: 0.664 ERA: 2.35 WHIP: 0.65 W: 0.0 L: 1.0 SV: 0.0
  ....
  Name: Jerad Eickhoff GS: 4.0 IP: 12.2 BF: 58.0 BB%: 6.897 K%: 10.345 FIP: 9.557 ERA: 4.97 WHIP: 1.66 W: 0.0 L: 1.0 SV: 0.0

  All free-agent batters:
  Name: Curt Casali PA: 45.0 wRC: 16.375 wRC/PA: 0.364 wOBA: 0.612 BABIP: 0.565 wRC+: 295.889
  Name: Garrett Cooper PA: 54.0 wRC: 18.372 wRC/PA: 0.34 wOBA: 0.583 BABIP: 0.6 wRC+: 278.776
  ....
  Name: Skye Bolt PA: 39.0 wRC: -1.937 wRC/PA: -0.05 wOBA: 0.105 BABIP: 0.133 wRC+: -35.18
