from numpy.lib.function_base import average
from pandas.io.parsers import read_csv
from constants import COL_NAMES, TEAMS, TEAMS_NAMES
import pandas as pd
import numpy as np

SEASONS = [
    "SEASON_20_21",
    "SEASON_19_20",
    "SEASON_18_19",
    "SEASON_17_18",
    "SEASON_16_17",
]

def create_df(seasons, columns):
    df = pd.DataFrame(columns = columns)
    for season in seasons:
        for team in TEAMS_NAMES:
            # print(team)
            df_team = read_csv(f"data/teams/{season}/{team}_score_posession.csv")
            arr = [list()] * len(columns)
            arr[0] = f"{team}"
            arr[1] = sum(df_team['score'].tolist())
            arr[2] = average(df_team['possession_percentage'].tolist())
            arr[3] = sum(df_team['attempts_ibox'].tolist())

            if (arr[2] != 0 and arr[3] > 150 and arr[1] > 5):
                df.loc[f"{team}{season[-2:]}"] = arr
    df.to_csv("data/score_shots.csv")
    print(df)


if __name__ == "__main__":
    create_df(SEASONS, ['team', 'score', 'possession_percentage', 'shots'])