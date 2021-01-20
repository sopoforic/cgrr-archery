archery
=======

This module reads and writes score files for Archery, a DOS game by Brian
Blankenship.

![Test](https://github.com/sopoforic/cgrr-archery/workflows/Test/badge.svg) [![Test Coverage](https://api.codeclimate.com/v1/badges/7b8a486c65bda82fd8f1/test_coverage)](https://codeclimate.com/github/sopoforic/cgrr-archery/test_coverage) [![Maintainability](https://api.codeclimate.com/v1/badges/7b8a486c65bda82fd8f1/maintainability)](https://codeclimate.com/github/sopoforic/cgrr-archery/maintainability)

Usage
=====

Verify that you have the supported version of the game:

```python
verify("path/to/archery") # Returns True or False
```

Extract scores into a dictionary:

```python
scores = extract_scores(path="path/to/archery")
```

Or, if you have just a score file:

```python
scores = extract_scores(scorepath="path/to/ARCHERY.SCR")
```

Write a new score table to a file:

```python
scores = [
    {'score': 84, 'name': 'SomeName'},
    {'score': 47, 'name': 'Another'},
]
data = write_scores(scores)
with open("path/to/ARCHERY.SCR", "wb") as scorefile:
    scorefile.write(data)
```

Requirements
============

* Tested with Python 3.5-3.9
* cgrr from https://github.com/sopoforic/cgrr
    * `pip install git+git://github.com/sopoforic/cgrr.git`


License
=======

This module is available under the GPL v3 or later. See the file COPYING for
details.
