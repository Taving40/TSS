from os.path import exists
import sqlite3
import sys

def dump_db(path, rename_to=None):
    """Expects a single argument: the relative path to the db that should be dumped.
       Will create the dump file on the same directory level that this script is located on."""
    if not exists(path):
        raise Exception("No such file")

    con = sqlite3.connect(path)
    rename_to = 'dump.sql' if not rename_to else rename_to
    with open(rename_to, 'w') as f:
        for line in con.iterdump():
            f.write('%s\n' % line)

def main():
    dump_db(sys.argv[1])
    

if __name__ == "__main__": 
    main()