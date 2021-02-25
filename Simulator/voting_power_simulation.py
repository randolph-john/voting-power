# TODO:
# add options for reapportionment and for DC + Puerto rico statehood

import math
import openpyxl
import pandas as pd
import random
import sys

# constants
# probability_column = 'Economist_prob_red'
# probability_column = '538_prob_red'
probability_column = 'Equal'
# EV_column = 'EV'
EV_column = 'EV_2024'
num_runs = 10000
sig_figs = 2
input_file_name = 'states.xlsx'
output_file_name = 'simulation_output.xlsx'

def main():
    if (len(sys.argv) > 1 and sys.argv[1] in ["banzhaf", "ss"]):
        df = pd.read_excel(input_file_name)
        df = df.set_index('State')
        if (len(sys.argv) > 2 and sys.argv[2].isnumeric()):
            global num_runs
            num_runs = int(sys.argv[2])
        if (sys.argv[1] == "banzhaf"):
            print('running Banzhaf Power Index simulation for {} runs...'.format(num_runs))
            state_to_num_tallies, wins = bh_power_index(df)
        elif sys.argv[1] == "ss":
            print('running Shapley-Shubik Power Index simulation for {} runs...'.format(num_runs))
            state_to_num_tallies, wins = ss_power_index(df)
    else:
        print("please pass \'banzhaf\' or \'ss\' as the first argument")
        print('second argument is optionally the number of runs (default {})'.format(num_runs))
        return
    print("saving...")
    calculate_and_print(df, state_to_num_tallies, wins, sys.argv[1])
    print("done!")

def ss_power_index(df):
    # import individual state probabilities
    sum_votes = sum(df[EV_column])
    win_number = int(math.ceil(sum_votes/2.0))

    state_to_num_tallies = dict()
    states = list(set(df.index))
    for state in states:
        state_to_num_tallies[state] = 0
    num_red_wins = 0
    num_blue_wins = 0
    num_ties = 0

    # run the simulations
    for i in range(num_runs):
        state_ordering = states
        random.shuffle(state_ordering)
        red_state_total = 0
        blue_state_total = 0

        for state in state_ordering:
            row = df.loc[state]
            if random.random() < row[probability_column]:
                red_state_total += row[EV_column]
            else:
                blue_state_total += row[EV_column]
            if (red_state_total >= win_number):
                state_to_num_tallies[state] += 1
                num_red_wins += 1
                break
            elif (blue_state_total >= win_number):
                state_to_num_tallies[state] += 1
                num_blue_wins += 1
                break
        if (blue_state_total == win_number and red_state_total > win_number):
            num_ties += 1

    return state_to_num_tallies, [num_red_wins, num_blue_wins, num_ties]


def bh_power_index(df):
    # import individual state probabilities
    df = pd.read_excel (input_file_name)
    df = df.set_index('State')

    sum_votes = sum(df[EV_column])
    win_number = int(math.ceil(sum_votes/2.0))

    state_to_num_tallies = dict()
    for state in df.index:
        state_to_num_tallies[state] = 0
    num_red_wins = 0
    num_blue_wins = 0
    num_ties = 0

    # run the simulations
    for i in range(num_runs):
        red_states = list()
        blue_states = list()
        red_state_total = 0
        blue_state_total = 0
        for _index, row in df.iterrows():
            if random.random() < row[probability_column]:
                red_states.append(row.name)
                red_state_total += row[EV_column]
            else:
                blue_states.append(row.name)
                blue_state_total += row[EV_column]
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
            if winning_total - df.loc[state, EV_column] < win_number:
                state_to_num_tallies[state] += 1

    return state_to_num_tallies, [num_red_wins, num_blue_wins, num_ties]

def calculate_and_print(df, state_to_num_tallies, wins, type):
    # sum and normalize for a couple things
    sum_tallies = float(sum(state_to_num_tallies.values()))
    state_overall_voting_power = dict()
    state_voting_power_pp = dict()
    for state in state_to_num_tallies:
        state_overall_voting_power[state] = state_to_num_tallies[state]/sum_tallies
    for state in state_overall_voting_power:
        state_voting_power_pp[state] = state_overall_voting_power[state]/float(df.loc[state, 'Population'])
    sum_voting_power_pp = float(max(state_voting_power_pp.values()))
    state_voting_power_pp.update((x, y/sum_voting_power_pp) for x, y in state_voting_power_pp.items())

    # export to excel
    out_df = pd.DataFrame(state_overall_voting_power.items())
    out_df = out_df.set_index(0)
    out_df.columns = ['Voting Power']
    out_df['Voting Power Per Person (normalized)'] = list(state_voting_power_pp.values())
    out_df = out_df.round(sig_figs)
    out_df.to_excel(output_file_name)

    # add some notes
    wb = openpyxl.load_workbook(filename=output_file_name)
    sheet = wb['Sheet1']
    sheet.append(['Red wins:', wins[0]])
    sheet.append(['Blue wins:', wins[1]])
    sheet.append(['Ties:', wins[2]])
    sheet.append(['Method:', 'Banzhaf Power Index' if type == 'banzhaf' else 'Shapley-Shubik Power Index'])
    sheet.column_dimensions["A"].width = 16
    sheet.column_dimensions["B"].width = 16
    sheet.column_dimensions["C"].width = 30
    wb.save(output_file_name)

if __name__ == '__main__':
    main()
