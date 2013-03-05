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
from unicodeMagic import UnicodeReader, UnicodeWriter
import hashlib


dataPath = os.path.abspath("../../data")

'''Github authors/committers (same person)'''
authors = set()
g = open(os.path.join(dataPath, 'githubUsers.csv'), 'rb')
reader = UnicodeReader(g)
for row in reader:
    authors.add(row[0])
print len(authors), 'Github users'
g.close()


'''SO users
    1;Jeff Atwood;51d623f33f8b83095db84ff35e15dbe8;21812;El Cerrito, CA;2008-07-31T14:22:31.287'''
so = {}
g = open(os.path.join(dataPath, 'SOUsers-Aug12.csv'), 'rb')
reader = UnicodeReader(g)
header = reader.next()
count = 0
for row in reader:
    id, name, ehash, rep, location, crdate = row
    '''There are multiple users with the same email hash: 
    they are considered as the same person'''
    if so.has_key(ehash):
        so[ehash].append([id, name, rep, location, crdate])
    else:
        so[ehash] = [[id, name, rep, location, crdate]]
    count += 1
        
print len(so.keys()), 'SO hashes', count, 'SO users'

parseFail = set()

'''Hash emails of Github authors, compute intersection'''
f = open(os.path.join(dataPath, 'SOIntersectionGithub.csv'), 'wb')
writer = UnicodeWriter(f)
header = ['unifiedId', 'githubEmail', 'SOUserIds']
writer.writerow(header)
counter = 0
for email in sorted(authors):
    try:
        m = hashlib.md5()
        m.update(email.lower())
        emailHash = m.hexdigest()
        if so.has_key(emailHash):
            row = [str(counter), email] + [','.join([userRow[0] for userRow in so[emailHash]])]
            writer.writerow(row)
            counter += 1
    except:
        parseFail.add(email)
f.close()
print counter, 'users in SO-Github intersection'


f = open(os.path.join(dataPath, 'SOIntersectionGithub-failed.csv'), 'wb')
writer = UnicodeWriter(f)
for email in sorted(parseFail):
    writer.writerow([email])
f.close()

print 'Done'

