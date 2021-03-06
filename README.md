Python API for the "Nuova CEI" (CEI 2008) Bible.  
Copyright © 2011-2015, Carlo Stemberger

python-cei2008 provides a simple and pythonic interface for downloading Bible
verses from the official website of the last Catholic Italian translation:

http://www.bibbiaedu.it/


Disclaimer
----------

python-cei2008 is free software, but please note that all rights of the Bible
translation used by it are reserved:

> Copyright © 2008, Fondazione di Religione Santi Francesco d'Assisi e Caterina
da Siena

The author does not encourage the violation of any laws. Only the final user is
responsable for any potential violations of the copyright law.


Dependencies
------------

You only need Python 3 (>= 3.4). On Debian/Ubuntu:
```
$ sudo aptitude install python3
```

Examples
--------

python-cei2008 is thought as a library:
```
>>> from cei2008 import CEI2008
>>> print(CEI2008('Matteo', 4, 4))
Ma egli rispose: "Sta scritto:

Non di solo pane vivrà l'uomo,
ma di ogni parola che esce dalla bocca di Dio".
```

However, it integrates also a simple CLI client:
```
$ ./cei2008.py 1_Corinzi 9 16-18
Infatti annunciare il Vangelo non è per me un vanto, perché è una necessità che mi si impone: guai a me se non annuncio il Vangelo! Se lo faccio di mia iniziativa, ho diritto alla ricompensa; ma se non lo faccio di mia iniziativa, è un incarico che mi è stato affidato. Qual è dunque la mia ricompensa? Quella di annunciare gratuitamente il Vangelo senza usare il diritto conferitomi dal Vangelo.
```
