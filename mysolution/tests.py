from normalizer import Normalizer

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
                # data example: [(None, None, False), 3, set([170, 11, 118]), set([7])]
                data = normalizer.normalize_raw(section_name, row_name)
                # We are looking for matches that result in `False` but are not caused by 
                # database returning multiple entries or row_name value passed as a range
                count = 0
                if data[0][2] == False and data[1] <=1 and '-' not in row_name:
                    count += 1
                    print data, section_name, row_name, row_name.isdigit()
            print 'BAD MATCH: ', count
            assert count == 0

if __name__ == "__main__":
    
    print 'TESTING DODGERS:'
    check_data('dodgerstadium_sections.csv', 'dodgertest.csv')

    print ''
    print 'TESTING CITI:'
    check_data('citifield_sections.csv', 'metstest.csv')
