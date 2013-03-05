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
import xml.etree.cElementTree as cElementTree
import os
from isoFilter import *
from unicodeMagic import UnicodeReader, UnicodeWriter
import unicodedata
import csv
from StringIO import StringIO


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
	uid = elem.get('Id', 0)
	rep = elem.get('Reputation', 0)
	name = elem.get('DisplayName', '')
	hash = elem.get('EmailHash', '')
	location = elem.get('Location', '')
	creation = elem.get('CreationDate','')
	
	if int(uid) != 0:
		row = [uid, name, hash, rep, location, creation]
		row = [unicode(part) for part in row]
		writer.writerow(row)
	

xmlPath = os.path.abspath('/Volumes/My Book/stackexchange/extracted/stackoverflow/users.xml')
dataPath = os.path.abspath("../../data")

f = open(os.path.join(dataPath, 'SOusers-Aug12.csv'), 'wb')
writer = UnicodeWriter(f)

fd = open(xmlPath, mode='rb')
context = etree.iterparse(fd)
fast_iter(context, process_element)

f.close()

