#!/usr/bin/env python

#    Copyright (C) 2011, Carlo Stemberger
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Python API for the "Nuova CEI" (CEI 2008) Bible.

This module provides a simple and pythonic interface for downloading Bible
verses from the official website of the last Catholic Italian translation.
"""

import urllib2
import BeautifulSoup as BS
from sys import argv

_cache = {}

class CEI2008(object):

    """An object representing Bible verses.

    book: a string chosen between 'Genesi', 'Esodo', 'Levitico', 'Numeri',
    'Deuteronomio', 'Giosue', 'Giudici', 'Rut', 'Samuele 1', 'Samuele 2',
    'Re 1', 'Re 2', 'Cronache 1', 'Cronache 2', 'Esdra', 'Neemia', 'Tobia',
    'Giuditta', 'Ester', 'Maccabei 1', 'Maccabei 2', 'Giobbe', 'Salmi',
    'Proverbi', 'Qoelet', 'Cantico_Dei_Cantici', 'Sapienza', 'Siracide',
    'Isaia', 'Geremia', 'Lamentazioni', 'Baruc', 'Ezechiele', 'Daniele',
    'Osea', 'Gioele', 'Amos', 'Abdia', 'Giona', 'Michea', 'Naum', 'Abacuc',
    'Sofonia', 'Aggeo', 'Zaccaria', 'Malachia', 'Matteo', 'Marco', 'Luca',
    'Giovanni', 'Atti_degli_Apostoli', 'Romani', 'Corinzi 1', 'Corinzi 2',
    'Galati', 'Efesini', 'Filippesi', 'Colossesi', 'Tessalonicesi 1',
    'Tessalonicesi 2', 'Timoteo 1', 'Timoteo 2', 'Tito', 'Filemone',
    'Ebrei', 'Giacomo', 'Pietro 1', 'Pietro 2', 'Giovanni 1', 'Giovanni 2',
    'Giovanni 3', 'Giuda' or 'Apocalisse';

    chapter: the chapter number;

    verses: an integer representing the verse number or a tuple representing
    the first and the last verse.
    """

    def __init__(self, book, chapter, verses):
        self.url = (
                'http://www.bibbiaedu.it/pls/bibbiaol/GestBibbia09.Ricerca?'
                'Libro={0}&Capitolo={1}'.format(book.replace(' ', '%20'),
                    chapter))
        try:
            self.soup = _cache[book, chapter]
        except:
            self.soup = BS.BeautifulSoup(
                    urllib2.urlopen(self.url).read().replace('<dd>', ''))
            _cache[book, chapter] = self.soup
        self.verses = verses

    def __str__(self):
        return ''.join(self.get_verses()).rstrip('\n ')

    def get_raw_verse(self, number):
        """Return the verse as a not well formatted string."""
        contents = self.soup.find('div', {'class': 'testo'}).contents
        parts = []
        for i in enumerate(contents):
            if 'name="VER_{0}"'.format(number) in str(i[1]):
                n = i[0] + 1
                while (isinstance(contents[n], BS.NavigableString) or
                        str(contents[n]) == '<br />' or
                        str(contents[n]).startswith('<i>')):
                    parts.append(str(contents[n]).replace(
                        '<br />', '\n').replace('<i>', '').replace('</i>', ''))
                    n += 1
                return ''.join(parts)

    def get_verses(self):
        """Return a list of the verses."""
        verses = []
        if isinstance(self.verses, tuple):
            first_verse, last_verse = self.verses
            for i in range(first_verse, last_verse + 1):
                verses.append(self.get_raw_verse(i))
        else:
            verses.append(self.get_raw_verse(self.verses))
        return verses

if __name__ == '__main__':
    if '-' in argv[3]:
        verses = tuple(int(i) for i in argv[3].split('-'))
    else:
        verses = int(argv[3])
    print CEI2008(argv[1].replace('_', ' '), int(argv[2]), verses)
