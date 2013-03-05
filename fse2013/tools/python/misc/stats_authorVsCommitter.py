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
from unicodeMagic import UnicodeReader, UnicodeWriter
import os

dataPath = os.path.abspath("../../data")

collectionNames = sorted(MyFolder(os.path.join(dataPath, 'github-commits')).baseFileNames('*.csv'))

g = open(os.path.join(dataPath, 'authorAndCommitterAreDifferent.csv'), 'wb')
writer = UnicodeWriter(g)

h = open(os.path.join(dataPath, 'authoredDateAndCommittedDateAreDifferent.csv'), 'wb')
writer2 = UnicodeWriter(h)

ok = 0
notok = 0

dateok = 0
datenotok = 0

for collection in collectionNames:
    print collection
    f = open(os.path.join(dataPath, 'github-commits', collection), 'rb')
    reader = UnicodeReader(f)
    header = reader.next()
    idx = 0
    for row in reader:
        try:
            c_email = row[3]
            a_email = row[7]
            if c_email != a_email:
                writer.writerow(row)
                notok += 1
            else:
                ok += 1
                
            c_date = row[4]
            a_date = row[8]
            if c_date != a_date:
                writer2.writerow(row)
                datenotok += 1
            else:
                dateok += 1
                
        except:
            print 'Line %d:' % (idx+2), row
            exit()
        idx += 1

g.close()
    
print '#commits:'

print 'author == committer:', ok
print 'author != committer:', notok

print 'authored date == committed date:', dateok
print 'authored date != committed date:', datenotok

