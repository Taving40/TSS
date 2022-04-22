import unittest
import sqlite3
import os
from unittest.mock import patch, MagicMock
import backend
import filecmp
from dump_db import dump_db
from shutil import copyfile

#for doc: https://www.toolsqa.com/software-testing/istqb/equivalence-partitioning/

class BackendUnitTestsFunctional(unittest.TestCase):

    #NOTE: Most of the functions make use of global variables
    #      Although these are not strictly parameters passed to the functions,
    #      They are expected to have a certain state when being accessed by the function
    #      So in some cases they should be considered when determining equivalence partitioning

    def test_connect_database_connection(self):
        #entries:
        #db_path       -> path to a file -> can have a correct or incorrect affix (.db):
        #              -> D_1 = { d | d~"*.db"}
        #              -> D_2 = { d | d!~"*.db"}
        #global conn  |
        #global cur   |-> entry value for all three is irrelevant as they get overwritten
        #global acc_no|

        #exits: 
        #global conn  |
        #global cur   |-> no influence (following the intended logic of the function, these would always be a Connection and Cursor objects)
        #global acc_no -> 1 or >1 -> splits into two classes, the specified path exists or not:
        #              -> C_1 = { db_path | db_path file exists}
        #              -> C_2 = { db_path | db_path file doesn't exist}

        def set_up():
            backend.acc_no, backend.conn, backend.cur = None, None, None

        #equivalance partitions:
        #C_11 = {(db_path) | db_path \in D_1, db_path \in C_1} ###################################################################

        set_up()
        db_path = "db_stubs/functional/test_connect_database_exists"
        #make a copy of the stub
        copyfile(src=f"{db_path}.db",
                 dst=f"{db_path}_copy.db")

        backend.connect_database(f"{db_path}_copy.db") #call the function on the copy
        self.assertGreater(backend.acc_no, 1)

        #cleanup
        backend.conn.close()
        os.remove(f"{db_path}_copy.db")

        #C_12 = {(db_path) | db_path \in D_2, db_path \in C_1} ###################################################################

        set_up()
        db_path = "db_stubs/functional/test_connect_database_exists"
        #make a copy of the stub
        copyfile(src=f"{db_path}",
                 dst=f"{db_path}_copy")

        backend.connect_database(f"{db_path}_copy") #call the function on the copy
        self.assertGreater(backend.acc_no, 1)

        #cleanup
        backend.conn.close()
        os.remove(f"{db_path}_copy")

        #C_13 = {(db_path) | db_path \in D_1, db_path \in C_2} ###################################################################

        set_up()
        db_path = "db_stubs/functional/blablabla"

        backend.connect_database(f"{db_path}.db") 
        self.assertEqual(backend.acc_no, 1)

        #cleanup
        backend.conn.close()
        os.remove(f"{db_path}.db")

        #C_14 = {(db_path) | db_path \in D_2, db_path \in C_2} ###################################################################

        set_up()
        db_path = "db_stubs/functional/blablabla"

        backend.connect_database(f"{db_path}") 
        self.assertEqual(backend.acc_no, 1)

        #cleanup
        backend.conn.close()
        os.remove(f"{db_path}")
        
        
        


        
















if __name__ == '__main__':
    unittest.main()