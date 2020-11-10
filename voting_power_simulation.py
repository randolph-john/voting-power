# imports
import math
import pandas as pd
import random

# constants
ECONOMIST = False # true if economist, false if fivethityeight
num_runs = 10000

def main():
    # import individual state probabilities
    df = pd.read_excel (r'states.xlsx')
    df = df.set_index('State')

    # TODO: add options for reapportionment, DC + Puerto rico statehood

    sum_votes = sum(df['EV'])
    win_number = int(math.ceil(sum_votes/2.0))

    # APPROACH 1: Banzhaf Power Index
    # for each state in winning coalition, tally
    # for each state, divide by population
    # output power for each state and for each voter

    state_to_num_tallies = dict()
    for state in df.index:
        state_to_num_tallies[state] = 0

    # calculating some random stats
    num_red_wins = 0
    num_blue_wins = 0
    num_ties = 0

    for i in range(num_runs):
        red_states = list()
        blue_states = list()
        red_state_total = 0
        blue_state_total = 0
        for _index, row in df.iterrows():
            flip = random.random()
            if (ECONOMIST and flip < row['Economist_prob_red']) or (not ECONOMIST and flip < row['538_prob_red']):
                blue_states.append(row.name)
                red_state_total += row['EV']
            else:
                red_states.append(row.name)
                blue_state_total += row['EV']
        if red_state_total > win_number:
            winning_coalition = red_states
            winning_total = red_state_total
            num_red_wins += 1
        elif blue_state_total >= win_number:
            winning_coalition = blue_states
            winning_total = blue_state_total
            num_blue_wins += 1
        else:
            winning_coalition = list()
            winning_total = 269
            num_ties += 1
        for state in winning_coalition:
            if winning_total - df.loc[state, 'EV'] < win_number:
                state_to_num_tallies[state] += 1

    print('Red wins {} times'.format(num_red_wins))
    print('Blue wins {} times'.format(num_blue_wins))
    print('{} ties'.format(num_ties))
    print(state_to_num_tallies)

if __name__ == '__main__':
    main()
