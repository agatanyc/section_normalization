"Section Normalization" - "normalize" the naming conventions applied by the various sellers and map the listings to a *canonical* list(i.e. manifest) of sections and rows that actually exist in the stadium. The sellers don't know about the manifest; they just type descriptions of the ticket into a text field.  This project uses rules and heuristics to normalize seller's descriptions and compare it with the manifest to determine if the ticket is valid.


## dependencies

python2

flask

sqlite3

## to initialize db and create tables run:

`python model.py`


