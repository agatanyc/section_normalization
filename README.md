"Section Normalization" - "normalize" the naming conventions applied by the various sellers and map the listings to a *canonical* list(i.e. manifest) of sections and rows that actually exist in the stadium. The sellers don't know about the manifest; they just type descriptions of the ticket into a text field.  This project uses rules and heuristics to normalize seller's descriptions and compare it with the manifest to determine if the ticket is valid.


## dependencies

python2

flask

sqlite3

sqlalchemy_utils


## GENERAL APPROACH 

I am saving parsed data from the manifests to my database and look for the match between the `normalize` function parameter pair (i.e (section_name, row_name)) and entry in the database.

## SECTION-name and ROW-name PARSING:

If there are digits in the text, I filter non-digits from that text and save only the digits in the section_name field. I have noticed cases of abbreviations i.e. entry in the dodgerstadium manifest `160,Left Field Pavilion 311,6,G` corresponds with valid sample entry `311PL,G,160,6,True`. Another reason for is approach is that both `Empire Suite 241` or `241` may be a considered valid input.
If we are saving any letters it all will be uppercase. 

In Dodgers Stadium data normalization I ran into issues where the database query results in multiple outputs that differ only by the section_id.  Below find an example output of my database query:

```
sqlite> select * from manifest where section_name='7' and row_name='N';
1342|107|7|12|N
2498|168|7|12|N
3062|201|7|12|N
```

Providing a solution to this problem would greatly complicate the code. In my test (see tests.py) I confirmed that this is the only cause of my script not finding the exact match. Note that the case where row_name is passed as a range(i.e. A-Z) is handled. A range value is never saved in the manifest therefore there will never be a match.




