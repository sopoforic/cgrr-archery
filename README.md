archery
=======

This module reads and writes score files for Archery, a DOS game by Brian
Blankenship.

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

License
=======

This module is available under the GPL v3 or later. See the file COPYING for details.
