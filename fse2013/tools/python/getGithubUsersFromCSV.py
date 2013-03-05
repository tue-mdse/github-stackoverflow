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

from folderUtils import MyFolder
from unicodeMagic import UnicodeWriter
import os
from dictUtils import MyDict
from dateutil.parser import parse
from unicodeMagic import UnicodeReader, UnicodeWriter

dataPath = os.path.abspath("../../data")

collectionNames = sorted(MyFolder(os.path.join(dataPath, 'github-commits')).baseFileNames('*.csv'))

authors = set()

for collection in collectionNames:
    print collection
    f = open(os.path.join(dataPath, 'github-commits', collection), 'rb')
    reader = UnicodeReader(f)
    header = reader.next()
    for row in reader:
        try:
            project, \
            c_login, c_name, c_email, c_date, \
            a_login, a_name, a_email, a_date = row
            if c_email == a_email:
                authors.add(a_email)
                
        except:
            print 'Line %d:' % (idx+2), row
            exit()

g = open(os.path.join(dataPath, 'githubUsers.csv'), 'wb')
writer = UnicodeWriter(g)
for email in sorted(authors):
    writer.writerow([email])
g.close()
    
print len(authors), 'authors'

