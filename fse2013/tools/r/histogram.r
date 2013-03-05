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

commitDates <- read.table("../../commitAuthoredDate.csv", sep=";", quote="\"", head=TRUE)
head(commitDates)
nc <- rep(1, length(commitDates$date))
df <- data.frame(date=commitDates$date, count=nc)
head(df)
df$date <- as.Date(df$date)

cs <- subset(df, date>=as.Date("2011/7/1"))
cs <- subset(cs, date<as.Date("2012/5/1"))

pdf("../../data/figures/commitsPerDay.pdf", width=7, height=4)
par(mar=c(4,4,0,0), oma=c(0,0,0,0))
hist(cs$date, "days", format="%b %y", freq=TRUE, main="", xlab="Date", ylab="Number of commits per day")
dev.off()

