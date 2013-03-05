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
from unicodeMagic import UnicodeWriter
import pickle

from timeSeries import TimeSeries


dataPath = os.path.abspath("../../data")

fdict = open(os.path.join(dataPath, 'timeseries.dict'), "r")
timeseries = pickle.load(fdict)
fdict.close()
print 'Load complete'


f = open(os.path.join(dataPath, 'rq1.csv'), 'wb')
writer = UnicodeWriter(f)
writer.writerow(['uid','numQ', 'numA', 'numC'])

for uid in sorted(timeseries.keys(), key=lambda elem:int(elem)):
    ts = timeseries[uid]
    counter = ts.countEvents()
    if counter['C'] > 0 and (counter['Q'] + counter['A'] > 0):
        row = [uid, counter['Q'], counter['A'], counter['C']]
        rowStr = [str(val) for val in row]
        writer.writerow(rowStr)

f.close()

print 'Done'

