# EECS 837 - Final project
## Theodore Lindsey

### About

This project reads lers-type files within the directory containing the python code and attempts to perform one of several discritizations on it:

* Global equal interval width
* Global equal frequency per interval
* Global conditional entropy

### Requirements

This program is compatible with 3.x (a small amount of tweaking should make it compatible with python
2.x). It is necessary to have both 
[```main.py```](https://github.com/RagingRoosevelt/eecs837_global-discretization/blob/master/main.py) 
and  
[```utility.py```](https://github.com/RagingRoosevelt/eecs837_global-discretization/blob/master/utility.py) 
in the same directory.  You should put any lers-type files in the same directory
as the two code files.  From there, simply run ```main.py``` and it should find
all ```.txt``` and ```.lers``` files.  It also has an option for manual filename 
entry for files in the same directory as the ```.py``` files.

### Running

Use ```$ python3 ./main.py``` to get started.

### [Assignment](http://people.eecs.ku.edu/~jerzy/proj-837.pdf)

### Notes

To the best of my knowledge, everything functions. Final remarks:
* equal frequency - The algorithm is wrong, I think.  It has problems with attribute values that have a huge covering compared to the other attribute values and it skews results to the first groupings when this occurs
* python versions - It shouldn't be difficult to get this working with python2.x.  In testing, the only problem appeared to be array indexes weren't being cast to ints properly.  I suspect this is because python 3.x and 2.x handle division differently (/ vs //)