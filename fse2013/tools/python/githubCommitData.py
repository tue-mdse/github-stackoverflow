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
from dictUtils import MyDict
from dateutil.parser import parse
from unicodeMagic import UnicodeReader, UnicodeWriter


connection = Connection()
db = connection['github']
collectionNames = sorted(db.collection_names())
collectionNames.remove('system.indexes')

commitSubcollections = [name for name in collectionNames if name.find('commits') != -1]


print len(collectionNames), 'items in collection'

collections = db.commits

parseFailed = 0
parseOk = 0

commitDates = MyDict()

dataPath = os.path.abspath("../../data")

header = ['path', 'c_login', 'c_name', 'c_email', 'c_date', 'a_login', 'a_name', 'a_email', 'a_date']


for collection in commitSubcollections:
    subCollection = collection.split('.')[1]
    print subCollection
    commits = collections[subCollection]
    
    f = open(os.path.join(dataPath, 'github-commits', '%s.csv' % subCollection), 'wb')
    writer = UnicodeWriter(f)
    writer.writerow(header)

    for commit in commits.find():
#        print commit['commit'].keys() [u'committer', u'added', u'author', u'url', u'tree', u'parents', u'committed_date', u'message', u'authored_date', u'id']
#        committer = commit['commit']['committer']
#        print committer.keys() [u'login', u'name', u'email']
#        author = commit['commit']['author']
#        print author.keys() [u'login', u'name', u'email']

        try:
            committer = commit['commit']['committer']
            committer_login = committer.get('login', 'NO_LOGIN')
            committer_name = committer.get('name', 'NO_NAME')
            committer_email = committer.get('email', 'NO_EMAIL')
            
            committed_date = commit['commit'].get('committed_date', 'NO_DATE')
            
            author = commit['commit']['author']
            author_login = author.get('login', 'NO_LOGIN')
            author_name = author.get('name', 'NO_NAME')
            author_email = author.get('email', 'NO_EMAIL')
            
            authored_date = commit['commit'].get('authored_date', 'NO_DATE')
            
#            cid = commit['commit']['id']
            url = commit['commit']['url']
#            "url" : "/mercurate/keyctrl/commit/2696e4aad4cea841c42f956604814239549e3fa7",
            project = url.split('/commit/')[0]
            
            writer.writerow([project, committer_login, committer_name, committer_email, committed_date, author_login, author_name, author_email, authored_date])
            parseOk += 1

        except:
            parseFailed += 1

    f.close()
    
    

print 'Successfully parsed:', parseOk, 'commits'
print 'Failed to parse:', parseFailed, 'commits'

