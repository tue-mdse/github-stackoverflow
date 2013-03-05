"""Copyright 2012-2013
Eindhoven University of Technology
Bogdan Vasilescu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

import os
import collections

dataPath = os.path.abspath("../../data")

import pickle
fdict = open(os.path.join(dataPath, 'githubActivity.dict'), "r")
ghActivity = pickle.load(fdict)
fdict.close()
print 'Loading done'

print len(ghActivity.keys()), 'Github+SO users'

for email in ghActivity.keys():
    dates = [a_date for (a_date, project) in ghActivity[email]]
    udates = set(dates)
    dupDates = [x for x, y in collections.Counter(dates).items() if y > 1]
    if len(dupDates):
        print email
        for (a_date, project) in sorted(ghActivity[email]):
            if a_date in dupDates:
                print a_date, project
        exit()


