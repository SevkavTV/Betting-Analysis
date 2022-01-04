from pandas.io.parsers import read_csv
from constants import TEAMS, TEAMS_NAMES
import pandas as pd
import numpy as np

SEASONS = [
    "SEASON_20_21",
    "SEASON_19_20",
    "SEASON_18_19",
    "SEASON_17_18",
    "SEASON_16_17",
]

def create_df(seasons):
    df = pd.DataFrame(columns = ['score', 'shots'])
    for season in seasons:
        for team in TEAMS_NAMES:
            # print(team)
            df_team = read_csv(f"data/teams/{season}/{team}_score_posession.csv")
            score = sum(df_team["score"].tolist())
            attempts_obox = sum(df_team["attempts_obox"].tolist())
            attempts_ibox = sum(df_team["attempts_ibox"].tolist())
            shots = attempts_ibox + attempts_obox / 2
            if (score != 0 and shots != 0):
                df.loc[f"{team}{season[-2:]}"] = [score, shots]
    df.to_csv("data/score_shots.csv")

if __name__ == "__main__":
    create_df(SEASONS)