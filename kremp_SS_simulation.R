# this file runs the Shapley-Shubik power index using the 
# update_prob function from Kremp

library("readxl")

setwd("~/Desktop/GitHub/kremp-polls")
source("update_prob.R")

num_runs = 50

# read in from excel
setwd("~/Desktop/GitHub/voting-power")
states <- read.csv("data/states.csv")
states <- cbind(states[-nrow(states),], num_picked = 0)
state_names <- states$State
competitive_states <- state_names[states$Economist_prob_red != 1.00 & states$Economist_prob_red != 0.00]
print(competitive_states)
rownames(states) <- states$State

# shapley-shubik function
for (i in 1:num_runs) {
  print(paste("iteration ", i))
  state_ordering <- sample(competitive_states)
  for (state in state_ordering) {
    red_states <- states$State[states$Economist_prob_red == 1.00]
    blue_states <- states$State[states$Economist_prob_red == 0.00]
    new_prob <- update_prob(clinton_states = blue_states, trump_states = red_states, show_all_states = TRUE)
    prob_clinton = new_prob[state]
    flip = runif(n=1,min=0,max=1)
    if (flip > prob_clinton) {
      states[state, "Economist_prob_red"] = 1.00
    } else {
      states[state, "Economist_prob_red"] = 0.00
    }
    
    red_total <- sum(states$EV[states$Economist_prob_red == 1.00])
    blue_total <- sum(states$EV[states$Economist_prob_red == 0.00])
    print(red_total)
    print(blue_total)
    
    if (red_total >= 270 || blue_total >= 270) {
      states[state, "num_picked"] <- (states[state, "num_picked"] + 1)
      print(paste(state, " was the deciding vote"))
      break
    }
  }
  print("here is the row")
  print(states$num_picked)
}

