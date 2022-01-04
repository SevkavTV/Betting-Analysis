from typing import Collection
import pandas as pd
from constants import TEAMS_NAMES, COL_NAMES

def get_team_data(df, team_name):
    df_team1 = df[df["team1"] == team_name]
    stats = [x + "1" for x in COL_NAMES]
    df_team1 = df_team1[["team1"] + stats]
    df_team1 = df_team1.set_axis([["team"] + COL_NAMES], axis = 1)

    
    df_team2 = df[df["team2"] == team_name]
    stats = [x + "2" for x in COL_NAMES]
    df_team2 = df_team2[["team2"] + stats]
    df_team2 = df_team2.set_axis([["team"] + COL_NAMES], axis = 1)

    # print(df_team1, df_team2)
    df_team = pd.concat([df_team1, df_team2])
    print(df_team)
    return df_team

def get_data(df):
    for team_name in TEAMS_NAMES[0:1]:
        df_team = get_team_data(df, team_name)
        create_team_csv(df_team, team_name)

def create_team_csv(df_team, filename):
    df_team.to_csv(f"data/teams/{filename}_stats.csv")

def read_csv(filename):
    df = pd.read_csv(filename)
    return df

if __name__ == "__main__":
    get_data(read_csv("data/matchesSEASON_20_21.csv"))