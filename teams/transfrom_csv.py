import pandas as pd

def wtf(f_name):
    df = pd.read_csv(f_name)
    d = dict()
    team_lst = df["team1"]
    team_lst = list(set(team_lst))
    for team_name in team_lst:
        df_team = df[df["team1"] == team_name]
        df_team = df_team[[

                    ### Overall ###
                    'team1',
                    'formation_used1',
                    'touches1',
                    'total_pass1',
                    "long_pass_own_to_opp_success1",

                    ### Agressive ###
                    "pen_area_entries1",
                    "final_third_entries1",
                    "total_fwd_zone_pass1",
                    "total_final_third_passes1",
                    "attempts_obox1", # outside box
                    "attempts_ibox1", # inside box
                    "fouled_final_third1",
                    "total_offside1",

                    ### defensive ###
                    'total_tackle1',
                    "blocked_pass1",
                    "interception1",
                    "total_back_zone_pass1",
                    "fk_foul_lost1", # team fouled, freekick against them
                    ]]
        df_team.to_csv(f'team/{team_name}_stats.csv', index=False)

if __name__ == "__main__":
    wtf("matches.csv")