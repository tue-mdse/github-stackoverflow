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


map = {}
email2id = {}
f = open(os.path.join(dataPath, 'SOIntersectionGithub.csv'), 'rb')
reader = UnicodeReader(f)
header = reader.next()
for row in reader:
    uid, ghEmail, soIdsStr = row
    map[ghEmail] = soIdsStr.split(',')
    email2id[ghEmail] = uid
f.close()

ghActivity = {}

histo = {}

collectionNames = sorted(MyFolder(os.path.join(dataPath, 'github-commits')).baseFileNames('*.csv'))
for collection in collectionNames:
    print collection
    f = open(os.path.join(dataPath, 'github-commits', collection), 'rb')
    reader = UnicodeReader(f)
    header = reader.next()
    idx = 0
    for row in reader:
        try:
            [project, \
            c_login, c_name, c_email, c_date, \
            a_login, a_name, a_email, a_date] = row
            shortDate = a_date.split()[0]
            if histo.has_key(shortDate):
                histo[shortDate] += 1
            else:
                histo[shortDate] = 1
            
            if c_email == a_email:
                if map.has_key(a_email):
                    id = email2id[a_email]
                    if ghActivity.has_key(id):
                        ghActivity[id].add((a_date, project))
                    else:
                        ghActivity[id] = set()
                        ghActivity[id].add((a_date, project))
        except:
            print 'Line %d:' % (idx+2), row
            exit()
        idx += 1


import pickle
fdict = open(os.path.join(dataPath, 'githubActivity.dict'), "w")
pickle.dump(ghActivity, fdict)
fdict.close()


f = open(os.path.join(dataPath, 'commitAuthoredDate.csv'), 'wb')
writer = UnicodeWriter(f)
writer.writerow(['date','count'])
for date in sorted(histo.keys()):
    writer.writerow([date, str(histo[date])])
f.close()    

print 'Done'