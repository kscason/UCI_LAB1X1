SIMPLESEM.py
=============

Documentation
-------------

SIMPLESEM.py
Interpreter for SIMPLESEM Language
UCI CSE 141
9 August 2016
Kaitlyn Cason
UCI Student ID: 20282205

COMPILATION: 
With version Python 2.7.10 on Mac OS X El Capitan, program
was compiled using the command: 
python SIMPLESEM.py Program#.S

Compared with other .Out files using the command:
python SIMPLESEM.py Program#.S | diff -w - Program#.S.Out

OUTPUT: 
SIMPLESEM.py outputs non-terminals to the standard output
line by line as they are processed. It uses python's print
function, so there is a new line after each non-terminal.

ERROR HANDLING: 
Some basic error handling is taken care of with TokenizerException
and ParserException. 

STRUCTURE:
SIMPLESEM is split up into LEXANALYZER and PARSER essentially, 
which perform the lexical analysis and parsing of SIMPLESEM
grammar rules respsectively.