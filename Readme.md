# Voting Power in the Electoral College
This project looks at voting power by state, by demographics, etc.

So far what has been done has been about looking at state voting power and state
voting power per person using probabilities from The Economist, 538, and equal
50/50, and using two methods: the Banzhaf Power Index and the Shapley-Shubik
Power Index.

See [this overleaf document](https://www.overleaf.com/project/5f8117bb557f6100010866bc)
for more in-depth description and other general notes.

## File tree
```
project
│   README.md - this readme
│   simulation_output.xlsx - output of simulation run by voting_power_simulation.py
│   states.xlsx - contains data on each state
|   voting_power_simulation.py - python script that updates simulation_output.xlsx
```

## Running the script
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
