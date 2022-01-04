from typing import Collection
import pandas as pd
from constants import TEAMS_NAMES, COL_NAMES

def get_team_data(df, team_name, data = COL_NAMES):
    df_team1 = df[df["team1"] == team_name]
    stats = [x + "1" for x in data]
    df_team1 = df_team1[stats]
    df_team1 = df_team1.set_axis([data], axis = 1)

    
    df_team2 = df[df["team2"] == team_name]
    stats = [x + "2" for x in data]
    df_team2 = df_team2[stats]
    df_team2 = df_team2.set_axis([data], axis = 1)

    # print(df_team1, df_team2)
    df_team = pd.concat([df_team1, df_team2])
    return df_team

def get_data(df, season_name = "", teams = TEAMS_NAMES, data = COL_NAMES):
    for team_name in teams:
        df_team = get_team_data(df, team_name, data)
        create_team_csv(df_team, team_name, season_name)

def create_team_csv(df_team, filename, season_name):
    df_team.to_csv(f"data/teams/{season_name}/{filename}_score_posession.csv", index = False)

def read_csv(filename):
    df = pd.read_csv(filename, index_col=False)
    return df

# def create_team_csv(df_team, filename):
#     df_team.to_csv(f"data/teams/{filename}_stats.csv")

if __name__ == "__main__":
    dat = ['team', 'score', 'attempts_ibox', 'attempts_obox']
    get_data(read_csv("data/matchesSEASON_20_21.csv"), "SEASON_20_21", data=dat)
    get_data(read_csv("data/matchesSEASON_19_20.csv"), "SEASON_19_20", data=dat)
    get_data(read_csv("data/matchesSEASON_18_19.csv"), "SEASON_18_19", data=dat)
    get_data(read_csv("data/matchesSEASON_17_18.csv"), "SEASON_17_18", data=dat)
    get_data(read_csv("data/matchesSEASON_16_17.csv"), "SEASON_16_17", data=dat)
