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


analysis <- function(eval){
  repetitions <- length(eval)-1
  vals <- eval[,1]
  lbl <- rep("real", length(vals))
  for (i in 1:repetitions+1){
    toAdd <- eval[,i]
    vals <- c(vals, toAdd)
    lbl <- c(lbl, rep(paste("sim_",i-2,sep=""), length(toAdd)))
  }
  data <- data.frame(vals, lbl)
  # head(data)
  
  res <- mctp(vals~lbl,data=data,type="Dunnett",asy.method="fisher",control="real",info=FALSE)
  #print(res)
  
  edges(res)
}

draw_boxplot <- function(eval, filename, mainlbl){  
  pdf(paste(imgFolder, filename, ".pdf",sep=""), width=8, height=6)
  par(mar=c(2,2,2,1))
  boxplot(eval, main=mainlbl, log="y",xlab="Time-series",ylab="Time",
          yaxt="n", ylim=c(1,3600*24*365))
  axis(2, at=c(1, 60, 3600, 3600*24, 3600*24*30, 3600*24*365), 
       labels=c("1 sec","1 min", "1 hour", "1 day", "1 month", "1 year"))
  dev.off()
}  


imgFolder <- "../../data/figures/"
dataFolder <- "../../data/"


# ASKING QUESTIONS

latencies <- read.table(paste(dataFolder, "evalLatencies20-Q.csv", sep=""), sep=";", quote="\"", header=TRUE)
draw_boxplot(latencies, "eval-questions50", "Evaluation latency: commits ~ asking questions")
analysis(latencies)

latencies <- read.table(paste(dataFolder, "respLatencies20-Q.csv", sep=""), sep=";", quote="\"", header=TRUE)
draw_boxplot(latencies, "resp-questions50", "Response latency: commits ~ asking questions")
analysis(latencies)

# ANSWERING QUESTIONS

latencies <- read.table(paste(dataFolder, "evalLatencies20-A.csv", sep=""), sep=";", quote="\"", header=TRUE)
draw_boxplot(latencies, "eval-answers50", "Evaluation latency: commits ~ answering questions")
analysis(latencies)

latencies <- read.table(paste(dataFolder, "respLatencies20-A.csv", sep=""), sep=";", quote="\"", header=TRUE)
draw_boxplot(latencies, "resp-answers50", "Response latency: commits ~ answers questions")
analysis(latencies)

# ACCEPTED ANSWERS TO QUESTIONS

latencies <- read.table(paste(dataFolder, "evalLatencies-accepted.csv", sep=""), sep=";", quote="\"", header=TRUE)
draw_boxplot(latencies, "eval-accepted", "Evaluation latency: commits ~ accepted answers")
analysis(latencies)

latencies <- read.table(paste(dataFolder, "respLatencies-accepted.csv", sep=""), sep=";", quote="\"", header=TRUE)
draw_boxplot(latencies, "resp-accepted", "Response latency: commits ~ accepted answers")
analysis(latencies)

