"Section Normalization" - "normalize" the naming conventions applied by the various sellers and map the listings to a *canonical* list(i.e. manifest) of sections and rows that actually exist in the stadium. The sellers don't know about the manifest; they just type descriptions of the ticket into a text field.  This project uses rules and heuristics to normalize seller's descriptions and compare it with the manifest to determine if the ticket is valid.


## dependencies

python2

flask

sqlite3

sqlalchemy_utils

## to initialize db and create tables run:

`python model.py`


In addition to seeing whether you solved the problem (and how accurately you normalized the listings), we're very interested to see *how* you attempted to solve it, and what kind of decomposition and code organization you used to implement the solution. On the first point, please submit a short (maybe 2 paragraph) README detailing your approach. Note that there are many different possibilities, and there are no bonus points for *complexity for its own sake*.

## SECTION PARSING:
* section_id is unique within a stadium
* section_id's start at 1
We are filtering non-digits from text, saving  only the integer as section_name value do that both `Empire Suite 241` or `241` are considered valid input.


## ROW PARSING:
* row_id is unique within a section
* row_id's are actually ordinal and start at 0, meaning row_id 0 is "closer to the front" than row_id 1
* some sections may have numerical row names (1-10) and some may have alphanumeric row names (A-Z, AA-DD). Your code should support both

Some rows are represented as numbers and some as upper_case letters (A-Z, AA-DD).
We assume Row A is an equivalent to row 1, Row Z to 26. If we see double letters we are passed Z therefore Row AA is equivalent to  27, BB to 28 and so forth..



