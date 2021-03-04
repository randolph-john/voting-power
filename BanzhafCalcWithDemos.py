# Calculates the Banzhaf Power Index one of two ways
# permutations() - runs for all permutations. Takes a long long time
# simulations() - estimates using monte carlo method. Converges pretty well
#                 with 500000 as num_simulations

import math
import random
import pandas as pd

# state -> (electoral votes, population)
states = {
    'AL': (6, 4903185),
    'AK': (3, 731545),
    'AZ': (11, 7278717),
    'AR': (6, 3017804),
    'CA': (55, 39512223),
    "CO": (9, 5758736),
    "CT": (7, 3565287),
    "DE": (3, 973764),
    "DC": (3, 705749),
    "FL": (29, 21477737),
    "GA": (16, 10617423),
    "HI": (4, 1415872),
    "ID": (4, 1787065),
    "IL": (20, 12671821),
    "IN": (11, 6732219),
    "IA": (6, 3155070),
    "KS": (6, 2913314),
    "KY": (8, 4467673),
    "LA": (8, 4648794),
    "ME": (4, 1344212),
    "MD": (10, 6045680),
    "MA": (11, 6892503),
    "MI": (16, 9986857),
    "MN": (10, 5639632),
    "MS": (6, 2976149),
    "MO": (10, 6137428),
    "MT": (3, 1068778),
    "NE": (5, 1934408),
    "NV": (6, 3080156),
    "NH": (4, 1359711),
    "NJ": (14, 8882190),
    "NM": (5, 2096829),
    "NY": (29, 19453561),
    "NC": (15, 10488084),
    "ND": (3, 762062),
    "OH": (18, 11689100),
    "OK": (7, 3956971),
    "OR": (7, 4217737),
    "PA": (20, 12801989),
    "RI": (4, 1059361),
    "SC": (9, 5148714),
    "SD": (3, 884659),
    "TN": (11, 6829174),
    "TX": (38, 28995881),
    "UT": (6, 3205958),
    "VT": (3, 623989),
    "VA": (13, 8535519),
    "WA": (12, 7614893),
    "WV": (5, 1792147),
    "WI": (10, 5822434),
    "WY": (3, 578759),
}

num_simulations = 500000

def permutations():
    states_counter = states.copy()
    for key in states_counter.keys():
        states_counter[key] = 0
    run_for_all_permutations_recursive([],[],list(states.keys()),states_counter)

# recursively generate all outcomes, then
def run_for_all_permutations_recursive(red_voters, blue_voters, remaining_states, states_counter):
    if not remaining_states:
        increment_outcome(red_voters,blue_voters,states_counter)
    else:
        new_state = remaining_states[0]
        run_for_all_permutations_recursive(red_voters + [new_state], blue_voters, remaining_states[1:], states_counter)
        run_for_all_permutations_recursive(red_voters, blue_voters + [new_state], remaining_states[1:], states_counter)

def increment_outcome(red_voters, blue_voters, states_counter):
    winners = []
    winning_total = 538
    red_total = 0
    blue_total = 0
    for state in red_voters:
        red_total += states[state][0]
    for state in blue_voters:
        red_total += states[state][0]
    if red_total >= 270:
        winners = red_voters
        winning_total = red_total
    elif blue_total >= 270:
        winners = blue_voters
        winning_total = blue_total
    for v in winners:
        if winning_total - states[v][0] < 270:
            # it is critical yes_voter
            states_counter[v] = states_counter[v] + 1

def simulations():
    # duplicate dictionary, set values to 0
    states_counter = states.copy()
    for key in states_counter.keys():
        states_counter[key] = 0

    tot_votes = 0
    for key in states.keys():
        tot_votes = tot_votes + states[key][0]

    nec_votes = math.ceil((float(tot_votes))/2.0)
    for i in range(num_simulations):
        yes_voters = []
        no_voters = []
        votes = 0
        for key in states.keys():
            if random.random() < .5:
            # if random.random() < states[key][1]:
                votes = votes + states[key][0]
                yes_voters.append(key)
            else:
                no_voters.append(key)
        # print("yes voters are ")
        # print(yes_voters)
        # print("votes are " + str(votes))
        if votes >= nec_votes:
            for v in yes_voters:
                if votes - states[v][0] < nec_votes:
                    # it is critical yes_voter
                    states_counter[v] = states_counter[v] + 1
        else:
            for v in no_voters:
                if votes + states[v][0] >= nec_votes:
                    # it is critical no_voter
                    states_counter[v] = states_counter[v] + 1
    tot_important = sum(states_counter.values())
    for key in states_counter.keys():
        states_counter[key] = states_counter[key]/tot_important

    df = pd.DataFrame(
        [{"state": index, "weight": value} for index, value in states_counter.items()]
    )
    print(df)
    df.to_csv('data/BHweights.csv', index=False)
    # divide and print for real value


if __name__ == '__main__':
    # permutations()
    simulations()
