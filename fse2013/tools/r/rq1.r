# Copyright 2012-2013
# Eindhoven University of Technology
# Bogdan Vasilescu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>."""

source("mctp.r")
source("edges.r")

# Load the data
df <- read.table("../../data/rq1.csv", sep=";", quote="\"", header=TRUE)
head(df)

# Create factors (labels) for <numChunks> groups
numChunks <- 4
numElems <- length(dfC$uid)
chunkSize <- round(numElems / numChunks)
labels <- c()
for (i in 1:(numChunks-1)){
  lbl <- paste("T",i,sep=" ")
  labels <- c(labels, rep(lbl, chunkSize))
}
labels <- c(labels, rep(paste("T",numChunks,sep=""), (numElems-chunkSize*(numChunks-1))))


# Sort by number of commits
dfC <- df[with(df, order(-numC)), ]
head(dfC)

# Split the #questions data into groups
values <- c()
for (i in 1:(numChunks-1)){
  values <- c(values, dfC$numQ[((i-1)*chunkSize+1):(i*chunkSize)])
}
values <- c(values, dfC$numQ[((numChunks-1)*chunkSize+1):(numElems)])
daf <- data.frame(values=values, labels=labels)

# Compare the different tiers to each other
res <- mctp(values~labels,data=daf,type="Tukey",asy.method="fisher")

# Print edges for ~T-graph
edges(res)


# Split the #answers data into groups
values <- c()
for (i in 1:(numChunks-1)){
  values <- c(values, dfC$numA[((i-1)*chunkSize+1):(i*chunkSize)])
}
values <- c(values, dfC$numA[((numChunks-1)*chunkSize+1):(numElems)])
daf <- data.frame(values=values, labels=labels)

# Compare the different tiers to each other
res <- mctp(values~labels,data=daf,type="Tukey",asy.method="fisher")

# Print edges for ~T-graph
edges(res)



# Sort by number of questions
dfQ <- df[with(df, order(-numQ)), ]
head(dfQ)

# Split the #commits data into groups
values <- c()
for (i in 1:(numChunks-1)){
  values <- c(values, dfQ$numC[((i-1)*chunkSize+1):(i*chunkSize)])
}
values <- c(values, dfQ$numC[((numChunks-1)*chunkSize+1):(numElems)])
daf <- data.frame(values=values, labels=labels)

# Compare the different tiers to each other
res <- mctp(values~labels,data=daf,type="Tukey",asy.method="fisher")

# Print edges for ~T-graph
edges(res)



# Sort by number of answers
dfA <- df[with(df, order(-numA)), ]
head(dfA)

# Split the #commits data into groups
values <- c()
for (i in 1:(numChunks-1)){
  values <- c(values, dfA$numC[((i-1)*chunkSize+1):(i*chunkSize)])
}
values <- c(values, dfA$numC[((numChunks-1)*chunkSize+1):(numElems)])
daf <- data.frame(values=values, labels=labels)

# Compare the different tiers to each other
res <- mctp(values~labels,data=daf,type="Tukey",asy.method="fisher")

# Print edges for ~T-graph
edges(res)

