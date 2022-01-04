from constants import TEAMS_NAMES, COL_NAMES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_stat(team, stat_name):
    df = pd.read_csv(f"./teams/{team}_stats.csv")
    df = df[stat_name]
    return df.tolist()

def get_data():
    d = dict()
    d_team = dict()

    for stat in COL_NAMES[2:]:
        for team in TEAMS_NAMES:
            data_lst = get_stat(team, stat)
            mean = np.nanmean(data_lst)
            try:
                d[stat].extend(data_lst)
                d_team[stat].append((team, mean))
            except KeyError:
                d[stat] = data_lst
                d_team[stat] = [(team, mean)]

        mean = np.nanmean(d[stat])
        d_team[stat].append(("General", mean))
    return d_team

def plot_data(d_team, stat):
    names = TEAMS_NAMES + ["General"]
    values = [x[1] for x in d_team[stat]]
    plt.plot(names, values)
    plt.show()

    # for stat, val in d_team.items():
    #     pass

if __name__ == "__main__":
    d_teams = get_data()
    print(d_teams)
    plot_data(d_teams, COL_NAMES[3])