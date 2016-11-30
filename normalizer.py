from model import Manifest, init_db, db
from app import app

class Normalizer(object):

    def __init__(self):
        pass

    def read_manifest(self, manifest):
        """Read a manifest file and populate the database.

        manifest should be a CSV containing the following columns
            * section_id
            * section_name
            * row_id
            * row_name

        Arguments:
            manifest {[str]} -- /path/to/manifest
        """
        with open(manifest, 'r') as f:
            manifest_file = f.read()
        if len(manifest_file) > 1:
            for line in manifest_file[1:]:
                # section_id,section_name,row_id,row_name
                elements = line.strip().split(',')
                #populate `manifest` table
                elements = (section_id,section_name,row_id,row_name)
                # EXTRACT THE NUMBER FROM SECTION NAME HERE!!!!!!
                current_line = Manifest(section_id=section_id,
                                        section_name=section_name,
                                        row_id=row_id,
                                        row_name=row_name)
                db.session.add(current_line)
                db.session.commit()


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

        ## your code goes here
        return (None, None, False)



    if __name__ == "__main__":
        app.debug = True

        init_db(app)
        app.run()

