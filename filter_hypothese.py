import pandas as pd


def filter_defensive(defensive_file: str):
    df = pd.read_csv(defensive_file)
    res_df = df[(df['first_half_goals1'] + df['first_half_goals2'] > 2)
                & (df['first_half_goals1'] > 0) & (df['first_half_goals2'] > 0)]
    res_df.to_csv('filter.csv')


def analyze_filter(filter_file: str):
    df = pd.read_csv(filter_file)
    success = 0
    for index, match in df.iterrows():
        diff = match['score1'] + match['score2'] - match['first_half_goals1'] - match['first_half_goals2']
        if diff < 2:
            success += 1
    
    print(success)


if __name__ == "__main__":
    filter_defensive('data/defensive.csv')
    analyze_filter('filter.csv')
