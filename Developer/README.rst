Endless Marvels Datasift Project
==============================

Initial Set Up
--------------

Install these with ``pip``::

    pip install datasift
    
    pip install PyMarvel
    
Info
----

Run endlessMarvels.py to get a list of Marvel characters, subscribe to a Datasift Twitter stream, and to record the results in json files

Files produced are:
- marvelChars - for a list of the Marvel characters
- twitterInteractions - a dump of all the interactions retrieved on the stream
- twitterUsefulData - the useful bits of the interactions for analysis

Challenges
----------

- An issue with the Marvel API, where character record 302 cannot be retrieved, so I skipped requesting that record

Things to do with more time!
----------------------------

This is mainly enhancing the csdl query...
- Lots of matches are for character names used in other contexts, e.g. "Speed" is probably going to match on many contexts that have nothng to do with the Marvel character
- On the other hand, "Spider-Man" is the character name from Marvel, but does this match with "Spider Man" as well?
- Optimisation of the csdl query would include removing character names that are really duplicates, e.g. "Spider-Man", "Spider-Man (Ai Apaec)", "Spider-Man (Ben Reilly)" etc could be condensed

Plus interpreting the results in more detail...
- Enhancements would be to weight retweets, authors based on Klout scores, followers etc