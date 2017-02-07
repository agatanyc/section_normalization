#!/usr/bin/env python

from string import ascii_uppercase
# some sections may have numerical ROW names (1-10) and some may have alphanumeric row names (A-Z, AA-DD). Your code should support both

def extract_integer(text):
    """Filters non-digits from text, and parses the result as an integer."""
    try:
      digits = ''.join(c for c in text if c.isdigit())
    except Exception:
      pass
    return int(digits)

def extract_integer_old(text):
    """Filters non-digits from text, and parses the result as an integer."""
    digits = ''.join(c for c in text if c.isdigit())
    if not digits:
        raise Exception("text is not numeric")
    return int(digits)

def parse_row_name(text):
    if not text:
        raise Exception("row number text is empty")
    elif all(c.isdigit() for c in text):
        return int(text)
    elif len(text) < 3 and all(c in ascii_uppercase for c in text):
        first = ord(text[0]) - ord(ascii_uppercase[0]) + 1
       # checking only for AA, BB, CC not AB, AC
       # if we have two characters we run out of letters e.i the Row is CC:
       # first = ord(C) - ord(ascii_uppercase[0]) + 1
       # first = 67 - 65 + 1
       # CC =  len(ascii_uppercase) +  first
       # CC = 26 + 3 => Row 29
        return first if len(text) < 2 else len(ascii_uppercase) + first
    else:
        raise Exception("bad row number: " + text)

def extract_row_name(text):
    row_names = ['AA', 'AB', 'AC', 'AD',
                 'BA', 'BB', 'BC', 'BD',
                 'CA', 'CB', 'CC', 'CD',
                 'DA', 'DB', 'DC', 'DD'
                  ]    
    if not text:
        raise Exception("row number text is empty")
    elif all(c.isdigit() for c in text):
        return int(text)
    elif len(text) < 3 and all(c in ascii_uppercase for c in text):
        first = ord(text[0]) - ord(ascii_uppercase[0]) + 1
        return first if len(text) < 2 else len(ascii_uppercase) + row_names.index(text) + 1
    else:
        raise Exception("bad row number: " + text)  

def get_upper(text):
    upper = (c.upper for c in text if c.isalpha())
    return upper

print 'XXXXX'
for s in get_upper('aaaa1'):
  print str(s)

assert extract_integer('Empire Suite 241') == 241
assert extract_integer('Empire Suite 2a41') == 241
assert parse_row_name('1') == 1
assert parse_row_name('10') == 10
assert parse_row_name('A') == 1
assert parse_row_name('DD') == 30
assert extract_row_name('AA') == 27
assert extract_row_name('AD') == 30

"""

| section           | row | n_section_id | n_row_id | valid |
|-------------------|-----|--------------|----------|-------|
| Section 432       | 1   | 215          | 0        | TRUE  |
| Section 432       | 2   | 215          | 1        | TRUE  |
| Section 432       | 99  | 215          |          | FALSE |
| Promenade Box 432 | 1   | 215          | 0        | TRUE  |
| sdlkjsdflksjdf    | 1   |              |          | FALSE |
| 432               | 1-5 | 215          |          | FALSE |
"""
