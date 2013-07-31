Gaikai Parser
=============

This module allows you to get a json of jobs listed at http://www.gaikai.com/careers and to search for a specific position.

Deps
----
```
$ pip install flask lxml supervisor
```

Run
---
```
$ supervisord
```

Usage
-----
To have a json with every job listed
[http://localhost:5000/jobs](http://localhost:5000/jobs)

To have a json looking for jobs matching a given set of words in the title (the search is case insensitive)
[http://localhost:5000/jobs/IT%20Manager](http://localhost:5000/jobs/IT%20Manager)
    