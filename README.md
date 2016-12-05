"Section Normalization" - "normalize" the naming conventions applied by the various sellers and map the listings to a *canonical* list(i.e. manifest) of sections and rows that actually exist in the stadium. The sellers don't know about the manifest; they just type descriptions of the ticket into a text field.  This project uses rules and heuristics to normalize seller's descriptions and compare it with the manifest to determine if the ticket is valid.


## dependencies

python2

flask

sqlite3

sqlalchemy_utils


## SECTION and ROW PARSING:

If there are digits in the text we filter non-digits from text, saving only the digits as section_name value. I noticed cases of abbreviations i.e. entry in the dodgerstadium manifest `160,Left Field Pavilion 311,6,G` corresponds with valid entry `311PL,G,160,6,True`. Another reason for is approach is that both `Empire Suite 241` or `241` may be a considered valid input.
If we are saving any letters it all will be uppercase. 


In Dodgers Stadium data normalization I run into issues where the database query results in multiple outputs that differ only be section_id.  Below find an output of my database query:

```
sqlite> select * from manifest where section_name='7' and row_name='N';
1342|107|7|12|N
2498|168|7|12|N
3062|201|7|12|N
```

I was not able to find a solution to this problem but in my test (see output of `_check_data` function) I confirmed that this is the only cause of my script not finding the exact match. Note that the case where row_name is passed as a range is handled. Range valued is never saved in the manifest therefore there will never be a match.




