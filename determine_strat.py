import pandas as pd


def set_strat():
    """
    """
    data = pd.read_csv(
        f"./data/means.csv", index_col=False)

    data['rating'] = 1/4*(data['final_third_entries'] +
                          data['attempts_obox'] +
                          data['attempts_ibox'] +
                          data['total_offside']) - 1/3*(data['total_tackle'] +
                                                        data['blocked_pass'] +
                                                        data['interception'])

    average = sum(list(data['rating'].values)) / len(data['rating'])
    strats = [1 if i >= average else 0 for i in data['rating'].values]

    data['strategy'] = strats

    result = data[['team', 'rating', 'strategy']]
    return result


def filter_matches(param):
    """
    """
    data = pd.read_csv(
        f"./data/matches.csv")
    strat_data = set_strat()

    data = pd.merge(data, strat_data, left_on='team1', right_on='team')
    data.rename(columns={"strategy": "strategy1",
                "rating": "rating1"}, inplace=True)
    del data["team"]

    data = pd.merge(data, strat_data, left_on='team2', right_on='team')
    data.rename(columns={"strategy": "strategy2",
                "rating": "rating2"}, inplace=True)
    del data["team"]

    return filter_data(data, param)


def filter_data(data, param):
    """
    """
    data = data[(data['strategy1'] == param) & (data['strategy2'] == param)]
    data = data[['team1', 'team2', 'score1', 'score2', 'rating1',
                 'rating2', 'strategy1', 'strategy2']].reset_index()
    del data['index']
    return data


if __name__ == '__main__':
    print(filter_matches(1))
    print(filter_matches(0))
