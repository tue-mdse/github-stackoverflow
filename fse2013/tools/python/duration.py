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

from unicodeMagic import UnicodeWriter
import os
from dateutil.parser import parse
from dateutil.tz import tzutc
import pytz
utc=pytz.UTC

from dateutil.relativedelta import *
#from datetime import datetime
import pickle

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
        date1 = parse(datestr)
        datesSet.add(date1)    
    
    for date1 in datesSet:
        if date1 >= bestAfter and date1 <= bestBefore:
            timeseries[uid].addEvent('C', date1)


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



f = open(os.path.join(dataPath, 'days.csv'), 'wb')
writer = UnicodeWriter(f)
writer.writerow(['uid', 'numDays'])

for unifiedId in timeseries.keys():
    ts = timeseries[unifiedId]
    counter = ts.countEvents()
    if counter['C'] > 1 and (counter['Q'] + counter['A'] > 0):
        commitDates = ts.orderedOccurrences('C')
        firstCommitDate = commitDates[0]
        lastCommitDate = commitDates[-1]
        delta = lastCommitDate - firstCommitDate
        writer.writerow([unifiedId, str(delta.days)])
        
f.close()

