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
from unicodeMagic import UnicodeWriter, UnicodeReader
from dateutil.parser import parse
import pickle

from dateutil.parser import parse
from dateutil.tz import tzutc
import pytz
utc=pytz.UTC

from timeSeries import TimeSeries

bestAfter = parse("2011-07-01", tzinfos=tzutc)
bestBefore = parse("2012-05-01", tzinfos=tzutc)


dataPath = os.path.abspath("../../data")


timeseries = {}

'''Commits'''
fdict = open(os.path.join(dataPath, 'githubActivity.dict'), "r")
ghActivity = pickle.load(fdict)
fdict.close()
print 'Loaded commits'

for uid, dates in ghActivity.items():
    if not timeseries.has_key(uid):
        timeseries[uid] = TimeSeries(uid)
        
    datesSet = set()
    for (datestr, project) in dates:
        date = parse(datestr)
        datesSet.add(date)    
    
    for date in datesSet:
        if date >= bestAfter and date <= bestBefore:
            timeseries[uid].addEvent('C', date)

'''Questions'''
fdict = open(os.path.join(dataPath, 'askingActivity.dict'), "r")
questionDates = pickle.load(fdict)
fdict.close()
print 'Loaded questions'

for uid, dates in questionDates.items():
    if not timeseries.has_key(uid):
        timeseries[uid] = TimeSeries(uid)
        
    for (datestr, qid) in dates:
        date = parse(datestr, tzinfos=tzutc)
        if date >= bestAfter and date <= bestBefore:
            timeseries[uid].addEvent('Q', date)

'''Answers'''
fdict = open(os.path.join(dataPath, 'answeringActivity.dict'), "r")
answerDates = pickle.load(fdict)
fdict.close()
print 'Loaded answers'

for uid, dates in answerDates.items():
    if not timeseries.has_key(uid):
        timeseries[uid] = TimeSeries(uid)
        
    for (datestr, qid) in dates:
        date = parse(datestr, tzinfos=tzutc)
        if date >= bestAfter and date <= bestBefore:
            timeseries[uid].addEvent('A', date)



import pickle
fdict = open(os.path.join(dataPath, 'timeseries.dict'), "wb")
pickle.dump(timeseries, fdict)
fdict.close()
print 'Serialised timeseries'


