# read in all past state voting outcomes

library('dplyr')

setwd("/Users/johnrandolph/Desktop/Github/voting-power")
states <- read.csv("data/states_past_voting.csv", stringsAsFactors = FALSE, header = TRUE)

n <- states$X
states <- as.data.frame(t(states[,-1]))
colnames(states) <- n
# states$myfactor <- factor(row.names(df.aree))

C <- cor(states)
C <- C[1:51,1:51]

# TODO:
# try in Economist's code
# k-means to create clusters