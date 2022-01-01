import requests
import pandas as pd

NUMBER_OF_MATCHES = 380
TEAMS = [
    1,      # Arsenal
    2,      # Aston Villa
    131,    # Brighton
    43,     # Burnley
    4,      # Chelsea
    6,      # Crystal Palace
    7,      # Everton
    34,     # Fulham
    9,      # Leeds United
    26,     # Leicester City
    10,     # Liverpool
    11,     # Manchester City
    12,     # Manchester United
    23,     # Newcastle United
    18,     # Sheffield United
    20,     # Southhampton
    21,     # Totenham Hotpurs
    36,     # West Bronwich Albion
    25,     # West Ham United
    38      # Wolverhampton Wanderers
    ]
SEASON_20_21_URL = f'https://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=363&teams=1,2,131,43,4,6,7,34,9,26,10,11,12,23,18,20,21,36,25,38&page=0&pageSize={NUMBER_OF_MATCHES}&sort=desc&statuses=C&altIds=true'
MATCH_STATISTICS_URL = "https://footballapi.pulselive.com/football/stats/match"

headers = {"origin": "https://www.premierleague.com"}
use_stats_names = ['formation_used',

                    ### Overall ###
                    'touches',
                    'total_pass',
                    "long_pass_own_to_opp_success",

                    ### Agressive ###
                    "pen_area_entries",
                    "final_third_entries",
                    "total_fwd_zone_pass",
                    "total_final_third_passes",
                    "attempts_obox", # outside box
                    "attempts_ibox", # inside box
                    "fouled_final_third",
                    "total_offside",

                    ### defensive ###
                    'total_tackle',
                    "blocked_pass",
                    "interception",
                    "total_back_zone_pass",
                    "fk_foul_lost", # team fouled, freekick against them
                    ]


def get_all_matches(season_url: str):
    matches = requests.get(season_url, headers=headers).json()['content']

    data = []
    for match in matches:
        match_id = int(match['id'])
        match_info = get_match_statistics(f'{MATCH_STATISTICS_URL}/{match_id}')
        data.append(match_info)

    return data


def get_match_statistics(match_url: str):
    data = requests.get(match_url, headers=headers).json()

    match_info = data['entity']
    stats_info = data['data']
    
    match_result = [
        match_info['teams'][0]['team']['name'], 
        match_info['teams'][1]['team']['name'],
        match_info['teams'][0]['score'],
        match_info['teams'][1]['score']
    ]
    stats_result = {key: [] for key in use_stats_names}


    for team_stat in stats_info.values():
        all_stats = team_stat['M']
        for stat in all_stats:
            if stat['name'] in use_stats_names:
                stats_result[stat['name']].append(stat['value'])

    return (match_result, stats_result)


def create_csv(matches):
    final_data = []
    csv_columns = ['team1', 'team2', 'score1', 'score2']
    for stat_name in use_stats_names:
        csv_columns.extend([f'{stat_name}1',
                            f'{stat_name}2'])

    for match in matches:
        final_match_data = match[0]
        stats_result = match[1]
        for stat_name in use_stats_names:

            try:
                final_match_data.extend([stats_result[stat_name][0]])
            except IndexError:
                final_match_data.extend([0])
            try:
                final_match_data.extend([stats_result[stat_name][1]])
            except IndexError:
                final_match_data.extend([0])

        final_data.append(final_match_data)

    df = pd.DataFrame(final_data, columns=csv_columns)
    df.to_csv('matches.csv', index=False)
    


if __name__ == '__main__':
    matches = get_all_matches(SEASON_20_21_URL)
    create_csv(matches)
