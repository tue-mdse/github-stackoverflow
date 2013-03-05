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

from pymongo import Connection
from unicodeMagic import UnicodeWriter
import os

connection = Connection()
db = connection['github']
collectionNames = sorted(db.collection_names())
collectionNames.remove('system.indexes')

print len(collectionNames), 'items in collection'

collections = db.commits

committers = set()
authors = set()

for collection in collectionNames:
    subCollection = collection.split('.')[1]
    print subCollection
    commits = collections[subCollection]
    
    for commit in commits.find():
        try:
            committer = commit['commit']['committer']
            tpl = (committer['login'], committer['name'], committer['email'])
            committers.add(tpl)
        except:
            if 'error' not in commit.keys() and 'actor' not in commit.keys():
                print commit.items()
        try:
            author = commit['commit']['author']
            tpl = (author['login'], author['name'], author['email'])
            authors.add(tpl)
        except:
            if 'error' not in commit.keys() and 'actor' not in commit.keys():
                print commit.items()
        
    
allUsers = authors.union(committers)

print len(committers), 'committers'
committers = sorted(committers, key=lambda elem: elem[1])

print len(authors), 'authors'
authors = sorted(authors, key=lambda elem: elem[1])

print len(allUsers), 'users overall'
allUsers = sorted(allUsers, key=lambda elem: elem[1])

dataPath = os.path.abspath("../../data")
header = ['username', 'name', 'email']

f = open(os.path.join(dataPath, "githubDump-committers.csv"), 'wb')
writer = UnicodeWriter(f)
writer.writerow(header)
for tpl in committers:
    row = []
    for elem in tpl:
        if elem is not None:
            row.append(elem)
        else:
            row.append("")
    writer.writerow(row)
f.close()

f = open(os.path.join(dataPath, "githubDump-authors.csv"), 'wb')
writer = UnicodeWriter(f)
writer.writerow(header)
for tpl in authors:
    row = []
    for elem in tpl:
        if elem is not None:
            row.append(elem)
        else:
            row.append("")
    writer.writerow(row)
f.close()

f = open(os.path.join(dataPath, "githubDump-all.csv"), 'wb')
writer = UnicodeWriter(f)
writer.writerow(header)
for tpl in allUsers:
    row = []
    for elem in tpl:
        if elem is not None:
            row.append(elem)
        else:
            row.append("")
    writer.writerow(row)
f.close()

