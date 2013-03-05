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

edges <- function(res){
  s_xy <- subset(res$Analysis, Upper < 0)
  names <- strsplit(rownames(s_xy), " - ")
  if (length(names) > 0){
    for (i in 1:length(names)){
      cat(paste("(\"",names[[i]][2],"\",",sep=""), paste("\"",names[[i]][1],"\")",sep=""), "\n")
    }
  }
  
  s_yx <- subset(res$Analysis, Lower > 0)
  names <- strsplit(rownames(s_yx), " - ")
  if (length(names) > 0){
    for (i in 1:length(names)){
      cat(paste("(\"",names[[i]][1],"\",",sep=""), paste("\"",names[[i]][2],"\")",sep=""), "\n")
    }
  }
}