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
                    section_id = elements[0]
                    # extract the number from the section name
                    s = elements[1]
                    section_name = extract_integer(s)
                    row_id = elements[2]
                    r = str(extract_row_name(elements[3]))
                    row_name = r
                    #populate `manifest` table
                    current_line = Manifest(section_id=section_id,
                                            section_name=section_name,
                                            row_id=row_id,
                                            row_name=row_name)
                    session.add(current_line)
                    session.commit()


    def normalize_raw(self, section, row):
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
        section = extract_integer(section)
        if row:
            parsed_row_name = str(extract_row_name(row)).upper()
        else:
            parsed_row_name = ''

        print "TESTING", section, parsed_row_name
        # query the db for all seats in passed section
        seats = session.query(Manifest).filter(Manifest.section_name == section
                                         and Manifest.row_name == parsed_row_name).all()
        result = []
        for seat in seats:
            result.append({'section_id' : seat.section_id,
                           'row_id' : seat.row_id,
                           'row_name' : seat.row_name})
        if len(result) == 0:
            section = extract_integer(section)
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
                return [(section_id, None, True),1, set([section_id]), set([])]
            else:
                row_id = result[0]['row_id']
                return [(section_id, row_id, True), 1, set([section_id]), set([row_id])]
        else:
            return find_one(result, parsed_row_name)

    def normalize(self, section, row):
        return self.normalize_raw(section, row)[0]



# Utility functions

def find_one(lst,  parsed_row):
    """(list of dict, str) ->
    Check there is exactly one match between row name in db and passed row."""
    # [number of found matches, section_id, row_id]
    count = [0, None, None]
    section_ids = []
    matched_row_ids = []
    for r in lst:
        if r['row_name'] == parsed_row:
            count[0] += 1
            count[1] = r['section_id']
            count[2] = r['row_id']
            # keep track how many different section id we have seen
            section_ids.append(r['section_id'])
            matched_row_ids.append(r['row_id'])
            # THIS LINE IS FOR TESTING< REMOVE:
            #if count[0] > 1:
            #    print ['count: ', count[0], 's_id: ',r['section_id'], 'r_id: ', r['row_id']], 'r_name:', r['row_name']
    if count[0] == 1:        
            return [(count[1], count[2], True), 1, set([count[1]]), set([count[2]])]
    else:
        # [(section_id, row_id, bool), number of matches, section ids we have seen, row_id we have seen]
        # len(section_ids) should equal count[0], len(row_ids) should equal 1
        return [(None, None, False), count[0], set(section_ids), set(matched_row_ids)]


def extract_row_name(text):
    """(str) -> str """
    text = str(text).strip()
    if text and all(c.isdigit() for c in text) and len(text) > 1:
        return text.lstrip('0')
    else:
        return text.upper()
   
def extract_integer(text):
    """Filters non-digits from text, and parses the result as an integer."""
    digits = ''.join(c for c in str(text) if c.isdigit())
    return digits if digits else text.upper()

def check_data(manifest, sample):
    normalizer = Normalizer()
    normalizer.read_manifest(manifest)
    with open(sample, 'r') as f:
        sample_file = f.read().strip()
        if len(sample_file) > 1:
            for line in sample_file.split('\n')[1:]:
                # line in the manifest: section_id,section_name,row_id,row_name
                line = line.strip()
                elements = line.split(',')
                section_name = elements[0]
                row_name = elements[1]
                # [(section_id, row_id, bool), number of matches, different section ids we have seen, different row_id we have seen]
                # len(section_ids) should equal count[0], len(row_ids) should equal 1
                # data example: [(None, None, False), 3, set([170, 11, 118]), set([7])]
                data = normalizer.normalize_raw(section_name, row_name)
                bad_match = 0
                if data[0][2] == False and data[1] <=1 and '-' not in row_name:
                    bad_match += 1
                    print data, section_name, row_name, row_name.isdigit()
            print 'BAD MATCH: ', bad_match
                
if __name__ == "__main__":
    n = Normalizer()
    print 'TESTING CITI:'
    n.read_manifest('citifield_sections.csv')
    print n.normalize('Caesars Box 326','7')

    print ''
    print 'TESTING DODGERS:'
    n.read_manifest('dodgerstadium_sections.csv')
    print n.normalize('Infield Box IFB29','B')

    """
    print 'TESTING DODGERS:'
    check_data('assignment/manifests/dodgerstadium_sections.csv', 'assignment/samples/dodgertest.csv')

    print ''
    print 'TESTING CITI:'
    check_data('assignment/manifests/citifield_sections.csv', 'assignment/samples/metstest.csv')
    """





    
