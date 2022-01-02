import pandas as pd
from pandas.core.algorithms import unique


def gen_mean(team):
    """
    """
    data = pd.read_csv(
        f"./teams/{team}_stats.csv")

    info = list(data.mean().values)
    info.insert(0, team)
    return info


def construct_means():
    """
    """
    cols = ['team', 'formation_used', 'touches', 'total_pass',
            'long_pass_own_to_opp_success', 'pen_area_entries',
            'final_third_entries', 'total_fwd_zone_pass',
            'total_final_third_passes', 'attempts_obox', 'attempts_ibox',
            'total_offside', 'total_tackle', 'blocked_pass', 'interception',
            'total_back_zone_pass', 'fk_foul_lost']

    data = pd.DataFrame(columns=cols)
    teams = unique(pd.read_csv("matches.csv")["team1"])

    for t in teams:
        mean = gen_mean(t)
        data = data.append({cols[i]: mean[i]
                           for i in range(len(cols))}, ignore_index=True)

    averages = [sum(list(data[cols[i]].values)) /
                len(list(data[cols[i]].values)) for i in range(1, len(cols))]

    for i, col in enumerate(cols):
        if i == 0:
            continue
        data[f"{col}_av_diff"] = (data[col] - averages[i-1])/averages[i-1]*100

    return data


def save_means():
    """
    """
    data = construct_means()
    data.to_csv('means.csv', index=False)


if __name__ == "__main__":
    print(save_means())
