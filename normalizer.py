from string import ascii_uppercase
from sqlalchemy_utils import database_exists
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()

class Manifest(Base):

    __tablename__ = 'manifest'

    primary_key = Column(Integer, autoincrement=True, primary_key=True)
    # section_id,section_name,row_id,row_name
    section_id = Column(Integer)
    section_name = Column(String(40))
    row_id = Column(Integer)
    row_name = Column(String(40))

def get_engine():
    return create_engine('sqlite:///manifest_data.db')

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def create_all():
    Base.metadata.create_all(get_engine())

session = init_db()

class Normalizer(object):
    def __init__(self):
        create_all()

    def read_manifest(self, manifest):
        """Read a manifest file and populate the database.

        manifest should be a CSV containing the following columns
            * section_id
            * sectreion_name
            * row_id
            * row_name

        Arguments:
            manifest {[str]} -- /path/to/manifest
        """
        session.query(Manifest).delete()
        with open(manifest, 'r') as f:
            manifest_file = f.read()
        if len(manifest_file) > 1:
            for line in manifest_file.split('\n')[1:]:
                # line in the manifest: section_id,section_name,row_id,row_name
                line = line.upper().strip()
                if line:
                    elements = line.split(',')
                    section_id = elements[0].upper()
                    # extract the number from the section name
                    section_name = elements[1]
                    row_id = elements[2]
                    r = str(extract_row_name(elements[3]))
                    row_name = r.upper()
                    #populate `manifest` table
                    current_line = Manifest(section_id=section_id,
                                            section_name=section_name,
                                            row_id=row_id,
                                            row_name=row_name)
                    session.add(current_line)
                    session.commit()


    def normalize(self, section, row):
        """normalize a single (section, row) input

        Given a (Section, Row) input, returns (section_id, row_id, valid)
        where
            section_id = int or None
            row_id = int or None
            valid = True or False

        Arguments:
            section {[type]} -- [description]
            row {[type]} -- [description]
        """
        found = False
        print 'NEW:'
        section = section.upper()
        if row:
            parsed_row_name = str(extract_row_name(row)).upper()
        else:
            parsed_row_name = ''
        # query the db for all seats in passed section
        seats = session.query(Manifest).filter(Manifest.section_name == section
                                         and Manifest.row_name == parsed_row_name).all()
        print 'section', section
        print 'SEATS', seats
        result = []
        for seat in seats:
            result.append({'section_id' : seat.section_id,
                           'row_id' : seat.row_id,
                           'row_name' : seat.row_name})
        if len(result) == 0:
            section = extract_integer(section)
            print 'extracted', section
            seats = session.query(Manifest).filter(Manifest.section_name == section
                                         and Manifest.row_name == parsed_row_name).all()
            result = []
            for seat in seats:
                result.append({'section_id' : seat.section_id,
                               'row_id' : seat.row_id,
                               'row_name' : seat.row_name})
            return find_one(result, parsed_row_name)
        elif len(result) == 1:
            section_id = result[0]['section_id']
            if result[0]['row_name'] == '':
                return (section_id, None, True)
            else:
                row_id = result[0]['row_id']
                return (section_id, row_id, True)
        else:
            print 'XXXXXX', 'HERE'
            return find_one(result, parsed_row_name)


            """
            count = [0, None, None]
            for r in result:
                print 'R', r, parsed_row_name
                if r['row_name'] == parsed_row_name:
                    print 'MATCHING_ROW', r['row_name']
                    count[0] += 1
                    count[1] = r['section_id']
                    count[2] = r['row_id']
            if count[0] == 1:        # and all(c.isalnum() or c in [' ', '&'] for c in row):
                print 'COUNT == 1'
                return (count[1], count[2], True)
            else:
                print count
                return (count[1], None, False)
"""
# Utility functions


def find_one(lst,  parsed_row):
    """(list of dict, str) ->
    Check there is exactly one match between row name in db and passed row."""
    count = [0, None, None]
    for r in lst:
        if r['row_name'] == parsed_row:
            count[0] += 1
            count[1] = r['section_id']
            count[2] = r['row_id']
    if count[0] == 1:        
            return (count[1], count[2], True)
    else:
        return (count[1], None, False)


def clean_text(text, bad_strings):
    """(str, list) -> str 
    Remove unwanted substrings from a string."""
    text = text.upper()
    for s in bad_strings:
        text = text.replace(s, '')
    return text

def extract_row_name(text):
    """(str) -> str """
    row_names = ['AA', 'AB', 'AC', 'AD',
                 'BA', 'BB', 'BC', 'BD',
                 'CA', 'CB', 'CC', 'CD',
                 'DA', 'DB', 'DC', 'DD'
                  ] 

    if text and all(c.isdigit() for c in str(text)):
        return text
    elif 1 < len(text) < 3 and all(c in ascii_uppercase for c in str(text)):
        try:
            first = ord(text[0]) - ord(ascii_uppercase[0]) + 1
            return first if len(text) < 2 else len(ascii_uppercase) + row_names.index(text) + 1
        except ValueError:
            pass
    else:
        return text

def extract_integer(text):
    """Filters non-digits from text, and parses the result as an integer."""
    digits = ''.join(c for c in str(text) if c.isdigit())
    return digits if digits else text

def get_upper(text):
    result = ''
    for c in text:
        if c.isalpha():
            result += c.upper()
        else:
            result += c
    return result


if __name__ == "__main__":
    manifest_city = 'citifield_sections.csv'
    manifest_doger = 'dodgerstadium_sections.csv'
    n = Normalizer()
    #n.read_manifest(manifest_city)
    #n.read_manifest(manifest_doger)
    
    print n.normalize('Excelsior Level 315','1')
    print n.normalize('524', '2')
    print n.normalize('Field Boxes 110','17')
    print n.normalize('417', '1')
    print n.normalize('60000000', '1')

# assertions for citifield manifest

    assert n.normalize('Excelsior Level 315','1')[2]
    assert n.normalize('524', '2')[2]
    assert n.normalize('Field Boxes 110','17')[2]
    assert n.normalize('417', '1')[2]
    assert not n.normalize('60000000', '1')[2]
    print 'the end'


    """
    Promenade Level 425,2,176,1,True
Excelsior Level 315,1,80,0,True
524,2,12,1,True
125,7,44,9,True
128,12,47,16,True
Field Boxes 110,17,87,21,True
417,1,93,0,True
519,4,137,3,True
328,5,203,4,True
"""




    
