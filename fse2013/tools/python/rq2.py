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
import pickle

from utils import percentile

from timeSeries import TimeSeries

bestAfter = parse("2011-07-01", tzinfos=tzutc)
bestBefore = parse("2012-05-01", tzinfos=tzutc)


dataPath = os.path.abspath("../../data")


#timeseries = {}
#
#
#'''Commits'''
#fdict = open(os.path.join(dataPath, 'githubActivity.dict'), "r")
#ghActivity = pickle.load(fdict)
#fdict.close()
#print 'Loaded commits'
#
#for uid, dates in ghActivity.items():
#    if not timeseries.has_key(uid):
#        timeseries[uid] = TimeSeries(uid)
#        
#    datesSet = set()
#    for (datestr, project) in dates:
#        date = parse(datestr)
#        datesSet.add(date)    
#    
#    for date in datesSet:
#        if date >= bestAfter and date <= bestBefore:
#            timeseries[uid].addEvent('C', date)
#
#
#'''Questions'''
#fdict = open(os.path.join(dataPath, 'askingActivity.dict'), "r")
#questionDates = pickle.load(fdict)
#fdict.close()
#print 'Loaded questions'
#
#for uid, dates in questionDates.items():
#    if not timeseries.has_key(uid):
#        timeseries[uid] = TimeSeries(uid)
#        
#    for (datestr, qid) in dates:
#        date = parse(datestr, tzinfos=tzutc)
#        if date >= bestAfter and date <= bestBefore:
#            timeseries[uid].addEvent('Q', date)
#
#'''Answers'''
#fdict = open(os.path.join(dataPath, 'answeringActivity.dict'), "r")
#answerDates = pickle.load(fdict)
#fdict.close()
#print 'Loaded answers'
#
#for uid, dates in answerDates.items():
#    if not timeseries.has_key(uid):
#        timeseries[uid] = TimeSeries(uid)
#        
#    for (datestr, qid) in dates:
#        date = parse(datestr, tzinfos=tzutc)
#        if date >= bestAfter and date <= bestBefore:
#            timeseries[uid].addEvent('A', date)
#
#
#'''Accepted answers'''
#fdict = open(os.path.join(dataPath, 'acceptingActivity.dict'), "r")
#accAnswerDates = pickle.load(fdict)
#fdict.close()
#print 'Loaded accepted answers'
#
#for uid, dates in accAnswerDates.items():
#    if not timeseries.has_key(uid):
#        timeseries[uid] = TimeSeries(uid)
#        
#    for (datestr, qid) in dates:
#        date = parse(datestr, tzinfos=tzutc)
#        if date >= bestAfter and date <= bestBefore:
#            timeseries[uid].addEvent('Z', date)


import pickle
fdict = open(os.path.join(dataPath, 'timeseries.dict'), "rb")
timeseries = pickle.load(fdict)
fdict.close()
print 'Finished loading'
        

def latencyAnalysis(eventType):
    simLbl = []
    for rep in range(repetitions):
        simLbl.append('sim_%d' % rep)
        
    f = open(os.path.join(dataPath, 'evalLatencies-%s.csv' % eventType), 'wb')
    writer1 = UnicodeWriter(f)
    writer1.writerow(['real'] + simLbl)
    
    g = open(os.path.join(dataPath, 'respLatencies-%s.csv' % eventType), 'wb')
    writer2 = UnicodeWriter(g)
    writer2.writerow(['real'] + simLbl)

    
    for unifiedId in timeseries.keys():
        ts = timeseries[unifiedId]
        counter = ts.countEvents()
        if counter['C'] > 1 and (counter['Q'] + counter['A'] > 0):
            [evaluation, response] = ts.computeLatencies(eventType, repetitions)
            
            numRows = max([len(l) for l in evaluation])
            if numRows:
                for i in range(numRows):
                    row = []
                    for j in range(repetitions+1):
                        try:
                            row.append(str(evaluation[j][i]))
                        except:
                            row.append('')
                    writer1.writerow(row)
        
            numRows = max([len(l) for l in response])
            if numRows:
                for i in range(numRows):
                    row = []
                    for j in range(repetitions+1):
                        try:
                            row.append(str(response[j][i]))
                        except:
                            row.append('')
                    writer2.writerow(row)
    f.close()
    g.close()


def groupByGithubPeriod(timeseries):
    deltas = []
    for unifiedId in timeseries.keys():
        ts = timeseries[unifiedId]
        counter = ts.countEvents()
        if counter['C'] > 1 and (counter['Q'] + counter['A'] > 0):
            commitDates = ts.orderedOccurrences('C')
            firstCommitDate = commitDates[0]
            lastCommitDate = commitDates[-1]
            delta = lastCommitDate - firstCommitDate
            deltas.append((unifiedId, delta.days))
    return sorted(deltas, key=lambda tpl:tpl[1])
    
        
def groupByAskingActivity(timeseries):
    deltas = []
    for unifiedId in timeseries.keys():
        ts = timeseries[unifiedId]
        counter = ts.countEvents()
        if counter['C'] > 1 and (counter['Q'] + counter['A'] > 0):
            deltas.append((unifiedId, counter['Q']))
    return sorted(deltas, key=lambda tpl:tpl[1])


def groupByAnsweringActivity(timeseries):
    deltas = []
    for unifiedId in timeseries.keys():
        ts = timeseries[unifiedId]
        counter = ts.countEvents()
        if counter['C'] > 1 and (counter['Q'] + counter['A'] > 0):
            deltas.append((unifiedId, counter['A']))
    return sorted(deltas, key=lambda tpl:tpl[1])


def groupByCommitActivity(timeseries):
    deltas = []
    for unifiedId in timeseries.keys():
        ts = timeseries[unifiedId]
        counter = ts.countEvents()
        if counter['C'] > 1 and (counter['Q'] + counter['A'] > 0):
            deltas.append((unifiedId, counter['C']))
    return sorted(deltas, key=lambda tpl:tpl[1])


        
        
def latencyAnalysisGroups(eventType, numGroups, groupFunc, repetitions, dataPath):
    simLbl = []
    for rep in range(repetitions):
        simLbl.append('sim_%d' % rep)
    
    evalFiles = {}
    evalWriters = {}
    respFiles = {}
    respWriters = {}
    
    for gr in range(1,numGroups+1):
        evalFiles[gr] = open(os.path.join(dataPath, 'evalLatencies-%s-%d.csv' % (eventType, gr)), 'wb')
        evalWriters[gr] = UnicodeWriter(evalFiles[gr])
        evalWriters[gr].writerow(['real'] + simLbl)

        respFiles[gr] = open(os.path.join(dataPath, 'respLatencies-%s-%d.csv' % (eventType, gr)), 'wb')
        respWriters[gr] = UnicodeWriter(respFiles[gr])
        respWriters[gr].writerow(['real'] + simLbl)
        
    deltas = groupFunc(timeseries)
    
    percentiles = []
    for gr in range(numGroups-1):
        percent = float(gr+1)/float(numGroups)
        fpercentile = functools.partial(percentile, percent=percent)
        percentiles.append(int(fpercentile(deltas, key=lambda tpl:tpl[1])))
    
    def getGroup(val, percentiles):
        if val > percentiles[-1]:
            return len(percentiles) + 1
        return [gr for gr, x in enumerate(percentiles) if val <= x][0]+1
            
    for (uid, value) in deltas:
        gr = getGroup(value, percentiles)
        
        ts = timeseries[uid]
        [evaluation, response] = ts.computeLatencies(eventType, repetitions)
        
        '''Evaluation latencies'''
        writer = evalWriters[gr]
        numRows = max([len(l) for l in evaluation])
        if numRows:
            for i in range(numRows):
                row = []
                for j in range(repetitions+1):
                    try:
                        row.append(str(evaluation[j][i]))
                    except:
                        row.append('')
                writer.writerow(row)
                
        '''Response latencies'''
        writer = respWriters[gr]        
        numRows = max([len(l) for l in response])
        if numRows:
            for i in range(numRows):
                row = []
                for j in range(repetitions+1):
                    try:
                        row.append(str(response[j][i]))
                    except:
                        row.append('')
                writer.writerow(row)
             
    for f in evalFiles.keys():
        evalFiles[f].close()
    for f in respFiles.keys():
        respFiles[f].close()




repetitions = 10

dataPath = os.path.abspath("../data/splitByGithubPeriod/latencies")
latencyAnalysisGroups('Q', 4, groupByGithubPeriod, repetitions, dataPath)
latencyAnalysisGroups('A', 4, groupByGithubPeriod, repetitions, dataPath)
latencyAnalysisGroups('Z', 4, groupByGithubPeriod, repetitions, dataPath)


dataPath = os.path.abspath("../data/splitByAskingActivity/latencies")
latencyAnalysisGroups('Q', 4, groupByAskingActivity, repetitions, dataPath)
latencyAnalysisGroups('A', 4, groupByAskingActivity, repetitions, dataPath)
latencyAnalysisGroups('Z', 4, groupByAskingActivity, repetitions, dataPath)


dataPath = os.path.abspath("../data/splitByAnsweringActivity/latencies")
latencyAnalysisGroups('Q', 4, groupByAnsweringActivity, repetitions, dataPath)
latencyAnalysisGroups('A', 4, groupByAnsweringActivity, repetitions, dataPath)
latencyAnalysisGroups('Z', 4, groupByAnsweringActivity, repetitions, dataPath)


dataPath = os.path.abspath("../data/splitByCommitActivity/latencies")
latencyAnalysisGroups('Q', 4, groupByCommitActivity, repetitions, dataPath)
latencyAnalysisGroups('A', 4, groupByCommitActivity, repetitions, dataPath)
latencyAnalysisGroups('Z', 4, groupByCommitActivity, repetitions, dataPath)



latencyAnalysis('Q')
latencyAnalysis('A')
latencyAnalysis('Z')


