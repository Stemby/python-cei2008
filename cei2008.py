#!/usr/bin/env python3

#    Copyright (C) 2011-2015, Carlo Stemberger
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

import urllib.request
import html
from sys import argv

_cache = {}

class CEI2008(object):

    """An object representing Bible verses.

    book: a string chosen between 'Genesi', 'Esodo', 'Levitico', 'Numeri',
    'Deuteronomio', 'Giosue', 'Giudici', 'Rut', '1 Samuele', '2 Samuele',
    '1 Re', '2 Re', '1 Cronache', '2 Cronache', 'Esdra', 'Neemia', 'Tobia',
    'Giuditta', 'Ester', '1 Maccabei', '2 Maccabei', 'Giobbe', 'Salmi',
    'Proverbi', 'Qoelet', 'Cantico_Dei_Cantici', 'Sapienza', 'Siracide',
    'Isaia', 'Geremia', 'Lamentazioni', 'Baruc', 'Ezechiele', 'Daniele',
    'Osea', 'Gioele', 'Amos', 'Abdia', 'Giona', 'Michea', 'Naum', 'Abacuc',
    'Sofonia', 'Aggeo', 'Zaccaria', 'Malachia', 'Matteo', 'Marco', 'Luca',
    'Giovanni', 'Atti_degli_Apostoli', 'Romani', '1 Corinzi', '2 Corinzi',
    'Galati', 'Efesini', 'Filippesi', 'Colossesi', '1 Tessalonicesi',
    '2 Tessalonicesi', '1 Timoteo', '2 Timoteo', 'Tito', 'Filemone',
    'Ebrei', 'Giacomo', '1 Pietro', '2 Pietro', '1 Giovanni', '2 Giovanni',
    '3 Giovanni', 'Giuda' or 'Apocalisse';

    chapter: the chapter number;

    verses: an integer representing the verse number or a tuple representing
    the first and the last verse.
    """

    def __init__(self, book, chapter, verses):
        self.url = (
                'http://www.bibbiaedu.it/testi/Bibbia_CEI_2008.ricerca?'
                'Libro={0}&Capitolo={1}'.format(book.replace(' ', '%20'),
                    chapter))
        try:
            self.webpage = _cache[book, chapter]
        except:
            self.webpage = urllib.request.urlopen(self.url).readlines()
            _cache[book, chapter] = self.webpage
        self.verses = verses

    def __str__(self):
        return ''.join(self.get_verses()).rstrip('\n ')

    def get_verse(self, number):
        """Return the desired verse."""
        for line in self.webpage:
            line = line.decode('latin_1')
            if 'name="VER_{}"'.format(number) in line:
                return html.unescape(line.split('</sup>')[1].replace(
                        '\n', '').replace('<br>', '\n').replace(
                        '<dd>', '').replace('<i> ', '').replace('</i> ', ''))

    def get_verses(self):
        """Return a list containing the verses."""
        verses = []
        if isinstance(self.verses, tuple):
            first_verse, last_verse = self.verses
            for i in range(first_verse, last_verse + 1):
                verses.append(self.get_verse(i))
        else:
            verses.append(self.get_verse(self.verses))
        return verses

if __name__ == '__main__':
    if '-' in argv[3]:
        verses = tuple(int(i) for i in argv[3].split('-'))
    else:
        verses = int(argv[3])
    print(CEI2008(argv[1].replace('_', ' '), int(argv[2]), verses))
