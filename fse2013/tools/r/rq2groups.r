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


analysis <- function(eval, label){
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
  print(label)
  edges(res)
}


evalBoxplots <- function(eventType, name, mainLbl, numGroups){
  for (i in 1:numGroups){
    fileName <- paste(name,"-", eventType, "-", i, ".csv", sep="")  
    df <- read.table(paste(dataFolder, fileName, sep=""), sep=";", quote="\"", header=TRUE)
    head(data)
    
    pdf(paste(imgFolder, fileName, ".pdf",sep=""), width=8, height=4.2)
    par(mar=c(2,2,2,1))
    m <- paste(mainLbl, " - Q", i, sep="")
    boxplot(df, main=m, log="y", xlab="Time-series", ylab="Time",
            yaxt="n", ylim=c(1,3600*24*365))
    axis(2, at=c(1, 60, 3600, 3600*24, 3600*24*30, 3600*24*365), 
         labels=c("1s","1m", "1h", "1d", "1mth", "1yr"))
    dev.off()
    a <- tryCatch(analysis(df, m), error=function(e) e)
    
  }
}

boxplots <- function(eventType, numGroups, label){
  evalBoxplots(eventType, "evalLatencies", paste("Evaluation latency: commits ~ ",label,sep=""), numGroups)
  print("")
  evalBoxplots(eventType, "respLatencies", paste("Response latency: commits ~ ",label,sep=""), numGroups)
}



# GROUPING BY TIME SPENT ON GITHUB (first-last commit)

imgFolder <- "~/github/github-stackoverflow/data/splitByGithubPeriod/boxplots/"
dataFolder <- "~/github/github-stackoverflow/data/splitByGithubPeriod/latencies/"

boxplots("Q", 4, "asking questions")
boxplots("A", 4, "answering questions")


# GROUPING BY QUESTION ASKING ACTIVITY

imgFolder <- "~/github/github-stackoverflow/data/splitByAskingActivity/boxplots/"
dataFolder <- "~/github/github-stackoverflow/data/splitByAskingActivity/latencies/"

boxplots("Q", 4, "asking questions")
boxplots("A", 4, "answering questions")


# GROUPING BY QUESTION ANSWERING ACTIVITY

imgFolder <- "~/github/github-stackoverflow/data/splitByAnsweringActivity/boxplots/"
dataFolder <- "~/github/github-stackoverflow/data/splitByAnsweringActivity/latencies/"

boxplots("Q", 4, "asking questions")
boxplots("A", 4, "answering questions")


# GROUPING BY COMMIT ACTIVITY

imgFolder <- "~/github/github-stackoverflow/data/splitByCommitActivity/boxplots/"
dataFolder <- "~/github/github-stackoverflow/data/splitByCommitActivity/latencies/"

boxplots("Q", 4, "asking questions")
boxplots("A", 4, "answering questions")

