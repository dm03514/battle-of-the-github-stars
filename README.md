# battle-of-the-github-stars

BATTLE OF THE GITHUB STARS

Create a django site that does the following:

1. Displays a page with a form consisting of two text inputs and a submission button.
    These inputs should accept github URLs in th	e format https://github.com/[USER]/[REPOSITORY]
2. On form submission, do the following:
	* Retrieve the number of stars each repository has on GitHub, using the GitHub API.
	    You can choose to query the API on the front end or the back end, your choice.
	* Compare the star counts of the two repositories
	* Compile statistics (star count, watcher count, fork count) for each of the
	    repositories, and inject a report into the DOM


----

Developed with

```python
Python 3.4.0 (default, Jun 19 2015, 14:20:21)
[GCC 4.8.2] on linux
```

### To Setup:

- clone repository
- install requirements (`pip install -r requirements`)

- run tests:

```python
$ python manage.py test
Creating test database for alias 'default'...
..........
----------------------------------------------------------------------
Ran 10 tests in 0.048s

OK
Destroying test database for alias 'default'...
```

- run server `python manage.py runserver`