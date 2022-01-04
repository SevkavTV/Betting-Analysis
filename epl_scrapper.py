import requests
import pandas as pd
from constants import COL_NAMES, TEAMS

NUMBER_OF_MATCHES = 380

SEASON_20_21_URL = f'https://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=363&teams=1,2,131,43,4,6,7,34,9,26,10,11,12,23,18,20,21,36,25,38&page=0&pageSize={NUMBER_OF_MATCHES}&sort=desc&statuses=C&altIds=true'
SEASON_19_20_URL = f'https://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=274&teams=1,2,131,43,4,6,7,34,9,26,10,11,12,23,18,20,21,36,25,38&page=0&pageSize={NUMBER_OF_MATCHES}&sort=desc&statuses=C&altIds=true'
SEASON_18_19_URL = f'https://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=210&teams=1,2,131,43,4,6,7,34,9,26,10,11,12,23,18,20,21,36,25,38&page=0&pageSize={NUMBER_OF_MATCHES}&sort=desc&statuses=C&altIds=true'
SEASON_17_18_URL = f'https://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=79&teams=1,2,131,43,4,6,7,34,9,26,10,11,12,23,18,20,21,36,25,38&page=0&pageSize={NUMBER_OF_MATCHES}&sort=desc&statuses=C&altIds=true'
SEASON_16_17_URL = f'https://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=54&teams=1,2,131,43,4,6,7,34,9,26,10,11,12,23,18,20,21,36,25,38&page=0&pageSize={NUMBER_OF_MATCHES}&sort=desc&statuses=C&altIds=true'
MATCH_STATISTICS_URL = "https://footballapi.pulselive.com/football/stats/match"

headers = {"origin": "https://www.premierleague.com"}


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
    team1_id = str(match_info['teams'][0]['team']['id'])
    team2_id = str(match_info['teams'][1]['team']['id'])
    
    match_result = [
        match_info['teams'][0]['team']['name'], 
        match_info['teams'][1]['team']['name'],
        match_info['teams'][0]['score'],
        match_info['teams'][1]['score']
    ]
    stats_result = {key: [] for key in COL_NAMES}


    for team_id in (team1_id, team2_id):
        all_stats = stats_info[team_id]['M']
        for stat in all_stats:
            if stat['name'] in COL_NAMES:
                stats_result[stat['name']].append(stat['value'])

    return (match_result, stats_result)


def create_csv(matches, filename):
    final_data = []
    csv_columns = ['team1', 'team2', 'score1', 'score2']
    for stat_name in COL_NAMES:
        csv_columns.extend([f'{stat_name}1',
                            f'{stat_name}2'])

    for match in matches:
        final_match_data = match[0]
        stats_result = match[1]
        for stat_name in COL_NAMES:

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
    df.to_csv(f'data/matches{filename[:-4]}.csv', index=False)
    


if __name__ == '__main__':
    matches = get_all_matches(SEASON_20_21_URL)
    create_csv(matches, "SEASON_20_21_URL")
    matches = get_all_matches(SEASON_19_20_URL)
    create_csv(matches, "SEASON_19_20_URL")
    matches = get_all_matches(SEASON_18_19_URL)
    create_csv(matches, "SEASON_18_19_URL")
    matches = get_all_matches(SEASON_17_18_URL)
    create_csv(matches, "SEASON_17_18_URL")
    matches = get_all_matches(SEASON_16_17_URL)
    create_csv(matches, "SEASON_16_17_URL")
