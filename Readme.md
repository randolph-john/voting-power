# Voting Power in the Electoral College
This project looks at voting power by state, by demographics, etc.

So far what has been done has been about looking at state voting power and state
voting power per person using probabilities from The Economist, 538, and equal
50/50, and using two methods: the Banzhaf Power Index and the Shapley-Shubik
Power Index.

See [this overleaf document](https://www.overleaf.com/project/5f8117bb557f6100010866bc)
more in-depth description and other general notes.

## File tree
```
project
|   BanzhafCalc.py - calculates BH PI
|   BaselineCalc.py - calculates demographic-based power baseline
│   README.md - this readme
├── Correlation Matrix - looking at adjusting the way the Economist's model correlates states
│   ├── generate_correlation_matrix.R - generates correlation matrix between states
│   ├── various_correlations_output.xlsx - output of different runs with different correlation matrices
│   ├── Kremp_SS_simulation.R - runs simulation using correlation matrix
│   └── data
│       ├── states_past_voting_after_flip.csv/xlsx - how states have voted since 1992
│       ├── states_past_voting.csv/xlsx - how states have voted since 1964
│       └── states.csv/xlsx - basic info about states
├── Simulator - looking at simulating BH/SS index based on likelihood of states to flip in 2020 election
│   ├── voting_power_simulation.py - run simulation
│   └── simulation_output.xlsx - output of simulation
├── data
│   ├── acs_2013_variables.csv - demographic info from the Economist
│   ├── BHweights.csv - BH weights of states
│   ├── SSweights.csv - SS weights of states
│   └── states.csv - basic info about states
```

## BaselineCalc

Run `BaselineCalc` to output the baseline of voter power of different demographics using three methods: only looking at the electorate, using the BH index, and using the SS index. More info on that and results can be found in the [overleaf document](https://www.overleaf.com/project/5f8117bb557f6100010866bc) in `Baseline.tex`.


## Correlation Matrix

Run the script `generate_correlation_matrix` to generate the correlation matrix between the states. Then run `Kremp_SS_simulation.R` to see the output of a run with that correlation matrix.

The results of runs with several different correlation matrices are in `various_correlations_output.xlsx`.

## Simulator
Run the script `voting_power_simulation.py` directly.

The first argument should be either `banzhaf` or `ss`, which will determine
which method the script uses for determining voting power (Banzhaf or
Shapley-Shubik). The second argument optionally sets the number times to
simulate the electoral college outcome (default is 10000).

The output is the file `simulation_output.xlsx` with three columns:
- state name
- calculated voting power of that state
- calculated voting power of each voter in the state, normalized so that the
most impactful voter has a power of 1

The excel file also includes the number of red wins, blue wins, ties, and
the method used (Banzhaf or Shapley-Shubik).
