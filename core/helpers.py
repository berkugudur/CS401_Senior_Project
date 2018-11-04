import json 

def write_file(path, data):
    with open(path, 'w') as outfile:
        outfile.write(data)