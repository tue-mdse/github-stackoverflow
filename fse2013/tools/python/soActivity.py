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

from lxml import etree
from unicodeMagic import UnicodeWriter, UnicodeReader
import os

def fast_iter(context, func):
    # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    # Author: Liza Daly
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context

    
def process_element(elem):
    try:
        pid = elem.get('Id', 0)
        ptid = int(elem.get('PostTypeId', 0))
        uid = int(elem.get('OwnerUserId', 0))
        if uid != 0:
            unifiedId = email2id[soMap[uid]]
            datestr = elem.get('CreationDate', 0)
        
            if ptid == 1:
                # Question
                if questionDates.has_key(unifiedId):
                    questionDates[unifiedId].append((datestr, pid))
                else:
                    questionDates[unifiedId] = [(datestr, pid)]
                    
                accAnswerId = int(elem.get('AcceptedAnswerId', 0))
                if accAnswerId:
                    if accAnswers.has_key(unifiedId):
                        accAnswers[unifiedId].append((pid, accAnswerId))
                    else:
                        accAnswers[unifiedId] = [(pid, accAnswerId)]
                     
                
            elif ptid == 2:
                # Answer
                if answerDates.has_key(unifiedId):
                    answerDates[unifiedId].append((datestr, pid))
                else:
                    answerDates[unifiedId] = [(datestr, pid)]
                
    except:
        pass
    

def process_element2(elem):
    try:
        pid = elem.get('Id', 0)
        ptid = int(elem.get('PostTypeId', 0))
        datestr = elem.get('CreationDate', 0)
        if ptid == 2:
            # Answer
            if reverse.has_key(int(pid)):
                unifiedId = reverse[int(pid)]
                if accAnswerDates.has_key(unifiedId):
                    accAnswerDates[unifiedId].append((datestr, pid))
                else:
                    accAnswerDates[unifiedId] = [(datestr, pid)]
    except:
        pass
    


xmlPath = os.path.abspath('/Volumes/My Book/stackexchange/extracted/stackoverflow')
dataPath = os.path.abspath("../../data")


map = {}
email2id = {}
f = open(os.path.join(dataPath, 'SOIntersectionGithub.csv'), 'rb')
reader = UnicodeReader(f)
header = reader.next()
for row in reader:
    id, ghEmail, soIdsStr = row
    email2id[ghEmail] = id
    map[ghEmail] = soIdsStr.split(',')
f.close()

soMap = {}
for ghEmail in map.keys():
    for soid in map[ghEmail]:
        soMap[int(soid)] = ghEmail



questionDates = {}
answerDates = {}
accAnswers = {}
accAnswerDates = {}


fd = open(os.path.join(xmlPath, 'posts.xml'), mode='rb')
context = etree.iterparse(fd)
fast_iter(context, process_element)
fd.close()
print 'Parsing pass 1/2 done'

reverse = {}
for unifiedId in accAnswers.keys():
    for (pid, accAnswerId) in accAnswers[unifiedId]:
        reverse[accAnswerId] = unifiedId

fd = open(os.path.join(xmlPath, 'posts.xml'), mode='rb')
context = etree.iterparse(fd)
fast_iter(context, process_element2)
fd.close()
print 'Parsing pass 2/2 done'


import pickle

fdict = open(os.path.join(dataPath, 'askingActivity.dict'), "w")
pickle.dump(questionDates, fdict)
fdict.close()

fdict = open(os.path.join(dataPath, 'answeringActivity.dict'), "w")
pickle.dump(answerDates, fdict)
fdict.close()

#fdict = open(os.path.join(dataPath, 'acceptingActivity.dict'), "w")
#pickle.dump(accAnswerDates, fdict)
#fdict.close()

print 'Done'
