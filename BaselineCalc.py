import pandas as pd

# ************************* calculate national demographics *************************

pop_total = 324473400-3468963

demographic_cols = [
    'white_pct',
    'black_pct',
    'hisp_other_pct',
    'college_pct',
    'wwc_pct',
]

demos = [
    'white',
    'black',
    'hispanic or other',
    'college educated',
    'white working class',
]


demos_dict = {
    'white': 0.0,
    'black': 0.0,
    'hispanic or other': 0.0,
    'college educated': 0.0,
    'white working class': 0.0,
}

df = pd.read_csv (r'data/acs_2013_variables.csv')
df.drop(df.tail(1).index,inplace=True)

for _, row in df.iterrows():
    for i in range(5):
        demos_dict[demos[i]] += row[demographic_cols[i]]*row['pop_total']

for i in demos_dict.keys():
    demos_dict[i] = demos_dict[i]/pop_total

# THIS PRINTS NATIONAL DEMOGRAPHICS OF ELECTORATE
print("------------ NATIONAL DEMOGRAPHICS ------------")
print(demos_dict)

# ************************* calculate demos state-by state with BH weights *************************

bh_demos_dict = {
    'white': 0.0,
    'black': 0.0,
    'hispanic or other': 0.0,
    'college educated': 0.0,
    'white working class': 0.0,
}

bh_df = pd.read_csv(r'data/BHweights.csv')
bh_df = bh_df.set_index('state')

for _, row in df.iterrows():
    for i in range(5):
        bh_demos_dict[demos[i]] += row[demographic_cols[i]]*bh_df.loc[row['state']].at['weight']
print("------------ BANZHAF CALCULATIONS ------------")
print(bh_demos_dict)

# ************************* calculate demos state-by state with SS weights *************************

ss_demos_dict = {
    'white': 0.0,
    'black': 0.0,
    'hispanic or other': 0.0,
    'college educated': 0.0,
    'white working class': 0.0,
}

ss_df = pd.read_csv(r'data/SSweights.csv')
ss_df = ss_df.set_index('state')

for _, row in df.iterrows():
    for i in range(5):
        ss_demos_dict[demos[i]] += row[demographic_cols[i]]*ss_df.loc[row['state']].at['weight']

print("------------ SHAPLEY-SHUBIK CALCULATIONS ------------")
print(ss_demos_dict)
