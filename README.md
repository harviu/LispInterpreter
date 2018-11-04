# Lisp interpreter

## How to run the interpreter:

python3 interpreter.py

Use python 3.5

## Input and Output

The interpreter will accept list and normal lisp expression and return a normal lisp expression.

Special cases:
(1) will be accepted as a list with a single atom.
() will not be accepted

The seperator is \n$, $ appearing without \n will be regarded as exception.

\n$$ will take the last express and end the process.

The output or exception will be returned when the $ is read.

Should any error occur, the interpreter will skip to the next \n$ and start reading there. 

## evaluation

The interpreter will accept list and normal lisp expression and return a normal lisp expression.

The output or exception will be returned when the $ is read.

Should any error occur, the interpreter will skip to the next \n$ and start reading there. 

When output is 'NIL' or 'T', it will print False or True

When output is integer, it will print just the number