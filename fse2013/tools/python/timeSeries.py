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


from utils import pairwise
from random import shuffle
import itertools


class TimeSeries(object):
    def __init__(self, uid):
        self.user = uid
        self.events = {}
        self.counter = {}
        for eventType in ['C', 'Q', 'A']:
            self.counter[eventType] = 0        
        
    def addEvent(self, eventType, eventDate):
        '''Adds event to the time series'''
        self.events[eventDate] = eventType
        self.counter[eventType] += 1
        
    def getEvents(self, bestAfter=None, bestBefore=None):
        e = sorted([(t,et) for (t,et) in self.events.items()])
        if bestAfter is not None:
            e = [(t,et) for (t,et) in e if t >= bestAfter]
        if bestBefore is not None:
            e = [(t,et) for (t,et) in e if t <= bestBefore]
        return e
        
    def countEvents(self):
        '''Returns dictionary with event counts per event type'''
        return self.counter
    
    def orderedEventList(self):
        '''Returns list of events (C, Q, A) sorted chronologically'''
        return [self.events[eventDate] for eventDate in sorted(self.events.keys())]

    def orderedOccurrences(self, eventType):
        '''Returns list of dates events of a given type occurred, sorted chronologically'''
        return [d for d in sorted(self.events.keys()) if self.events[d] == eventType]

    def firstOccurrence(self, eventType):
        '''Returns the first date an event of given type occurred'''
        return self.orderedOccurrences(eventType)[0]
    
    def lastOccurrence(self, eventType):
        '''Returns the first date an event of given type occurred'''
        return self.orderedOccurrences(eventType)[-1]
    

    '''Only interesting if there are at least 2 commits by this person'''
    def computeLatencies(self, eventType, repetitions):
        commitDates = self.orderedOccurrences('C')
        
        evalLatencies = []
        respLatencies = []
        
        randEvalLatencies = {}
        randRespLatencies = {}
        for rep in range(repetitions):
            randEvalLatencies[rep] = []
            randRespLatencies[rep] = [] 

        
        '''Find all dates of questions asked on SO by this person, under all her SO accounts.
        Only look at questions asked after the earliest commit and before the latest commit'''
        questionDates = [d for d in self.orderedOccurrences(eventType)]

        '''Don't bother unless there is at least one question in between the first and last commits'''
        if len(questionDates) >= 2:
            for (startDate, endDate) in pairwise(commitDates):
                '''Keep commit dates as first and last; add all dates of in-between questions in between'''
                soEvents = [d for d in questionDates if d >= startDate and d <= endDate]
                btConsecCommits = sorted([startDate] + soEvents + [endDate])
                '''Compute the time deltas for each pair of consecutive events'''
                deltas = []
                for (d1, d2) in pairwise(btConsecCommits):
                    delta = d2 - d1
                    deltas.append(delta.total_seconds())
                                    
                '''<deltas> should have size len(btConsecCommits)-1; btConsecCommits has size at least 2 since it always contains startDate and endDate.
                So <deltas> is by default of size at least one, but it should be of size at least 2'''
                if len(deltas) > 1:
                    evalLatencies.append(deltas[0])
                    respLatencies.append(deltas[-1])
        
            '''Compute the time deltas for each pair of consecutive communication events'''
            deltas = []
            for (d1, d2) in pairwise(questionDates):
                delta = d2 - d1
                deltas.append(delta)
            
            for rep in range(repetitions):                    
                randomDeltas = list(deltas)
                shuffle(randomDeltas)

                '''Create a new time series using the random deltas'''
                randQueDates = [min(questionDates)]
                curDate = min(questionDates)
                for delta in randomDeltas:
                    curDate += delta
                    randQueDates.append(curDate)
                    
                for (startDate, endDate) in pairwise(commitDates):
                    '''Keep commit dates as first and last; add all dates of in-between questions in between'''
                    btConsecCommits = sorted([startDate] + [d for d in randQueDates if d >= startDate and d <= endDate] + [endDate])
            
                    '''Compute the time deltas for each pair of consecutive events'''
                    deltas2 = []
                    for (d1, d2) in pairwise(btConsecCommits):
                        delta = d2 - d1
                        deltas2.append(delta.total_seconds())
                                        
                    '''<deltas> should have size len(btConsecCommits)-1; btConsecCommits has size at least 2 since it always contains startDate and endDate.
                    So <deltas> is by default of size at least one, but it should be of size at least 2'''
                    if len(deltas2) > 1:
                        randEvalLatencies[rep].append(deltas2[0])
                        randRespLatencies[rep].append(deltas2[-1])
             
        le= []
        lr = []
        for rep in range(repetitions):
            le.append(randEvalLatencies[rep])
            lr.append(randRespLatencies[rep])
            
        evaluation = [evalLatencies] + le
        response = [respLatencies] + lr
        return [evaluation, response]
            
