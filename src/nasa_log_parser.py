import re


# method to parse the logs from source_file_name as save result as csv on target_file_name
def log_parser(source_file_name, target_file_name):
    print('Parsing file: [{}]'.format(source_file_name))

    # read source file and read all lines
    with open(source_file_name, encoding='ascii', errors='ignore') as file_log_Jul95:
        lines = file_log_Jul95.readlines()

    parsed_lines = list()  # create empty list to stored parsed data

    # append header as the first line of the new csv file
    parsed_lines.append('{},{},{},{},{}\n'.format('requester', 'timestamp', 'resource', 'response',
                                                  'response_size'))

    # iterate over the lines of the file to match line with regex pattern below
    for idx, line in enumerate(lines):
        try:
            # first remove break lines and other invisible characters if present
            line = line.replace('\n', '').replace('\t', '').replace('\r', '')
            line = ' '.join(line.split(' '))  # also remove double spaces
            # use regex and groups to separate the important data
            m = re.match(r'(\S*)\s-\s-\s\[(.*)\]\s\"(.*)\"\s(\d*)\s([\d-]*)', line)
            g = m.groups()
            parsed_line = '{},{},{},{},{}\n'.format(g[0], g[1], g[2], g[3], g[4])
            parsed_lines.append(parsed_line)
        except:
            # on exception, print malformed line and continue
            print('Line[{}] - [{}] is malformed and could not be parsed'.format(idx, line))

    # save parsed lines on target file
    with open(target_file_name, 'w') as tgt_file:
        tgt_file.writelines(parsed_lines)
    print('Parsed file saved as: [{}]'.format(target_file_name))
