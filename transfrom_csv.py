import pandas as pd

COL_NAMES = [

    ### Overall ###
    'team',
    'formation_used',
    'touches',
    'total_pass',
    "long_pass_own_to_opp_success",

    ### Agressive ###
    "pen_area_entries",
    "final_third_entries",
    "total_fwd_zone_pass",
    "total_final_third_passes",
    "attempts_obox",  # outside box
    "attempts_ibox",  # inside box
    "total_offside",

    ### defensive ###
    'total_tackle',
    "blocked_pass",
    "interception",
    "total_back_zone_pass",
    "fk_foul_lost",  # team fouled, freekick against them
]


def wtf(f_name):
    df = pd.read_csv(f_name)
    d = dict()
    team_lst = df["team1"]
    team_lst = list(set(team_lst))
    for team_name in team_lst:
        df_team1 = df[df["team1"] == team_name]
        df_team2 = df[df["team2"] == team_name]
        team1_cols = [x + "1" for x in COL_NAMES]
        team2_cols = [x + "2" for x in COL_NAMES]
        df_team1 = df_team1[team1_cols]
        df_team2 = df_team2[team2_cols]
        df_team1.columns = COL_NAMES
        df_team2.columns = COL_NAMES
        df_team = pd.concat([df_team1, df_team2])

        df_team.to_csv(f'teams/{team_name}_stats.csv', index=False)


if __name__ == "__main__":
    wtf("matches.csv")
