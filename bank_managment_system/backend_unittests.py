import unittest
import sqlite3
import os
from unittest.mock import patch, MagicMock
import backend
import filecmp
from dump_db import dump_db
from shutil import copyfile

#NOTE: remember to keep each test entirely self-contained
#NOTE: functions that are explicitly supposed to modify the database will be tested using stubs
#      (in db_stubs subdirectory) since the actual thing being tested is the query 
#NOTE: the stub dbs in db_stubs shouldnt be worked with directly, but instead a copy should be made and worked with

class BackendUnitTests(unittest.TestCase):

    #test that the global connection object is initialized properly
    def test_connect_database_connection(self):
        #make a copy of the stub
        copyfile(src="db_stubs/test_connect_database_connection.db",
                 dst="db_stubs/test_connect_database_connection_copy.db")

        backend.connect_database("db_stubs/test_connect_database_connection_copy.db") #call the function
        self.assertIsInstance(backend.conn, sqlite3.Connection) #check if it is the appropriate class

        #cleanup
        backend.conn.close()
        os.remove("db_stubs/test_connect_database_connection_copy.db")

    #test that the global cursor object for the connection is initialized properly
    def test_connect_database_cursor(self):
        #make a copy of the stub
        copyfile(src="db_stubs/test_connect_database_cursor.db",
                 dst="db_stubs/test_connect_database_cursor_copy.db")

        backend.connect_database("db_stubs/test_connect_database_cursor_copy.db")
        self.assertIsInstance(backend.cur, sqlite3.Cursor)

        #cleanup
        backend.conn.close()
        os.remove("db_stubs/test_connect_database_cursor_copy.db")

    #test that the global account number object is initialized properly
    def test_connect_database_account_number(self): 
        #make a copy of the stub
        copyfile(src="db_stubs/test_connect_database_account_number.db",
                 dst="db_stubs/test_connect_database_account_number_copy.db")

        backend.connect_database("db_stubs/test_connect_database_account_number_copy.db")
        self.assertIsInstance(backend.acc_no, int)

        #cleanup
        backend.conn.close()
        os.remove("db_stubs/test_connect_database_account_number_copy.db")

    #test that the global account number object has proper value
    def test_connect_database_account_number_value(self):
        #make a copy of the stub
        copyfile(src="db_stubs/test_connect_database_account_number_value.db",
                 dst="db_stubs/test_connect_database_account_number_value_copy.db")

        backend.connect_database("db_stubs/test_connect_database_account_number_value_copy.db")
        self.assertGreater(backend.acc_no, 0)

        #cleanup
        backend.conn.close()
        os.remove("db_stubs/test_connect_database_account_number_value_copy.db")

    #test that all the tables were created
    def test_connect_database_table_creation(self):
        #make a copy of the stub
        copyfile(src="db_stubs/test_connect_database_table_creation.db",
                 dst="db_stubs/test_connect_database_table_creation_copy.db")

        #call the function 
        backend.connect_database("db_stubs/test_connect_database_table_creation_copy.db")
        
        #dump the db so that it can be compared and check it against the pre-built dump
        dump_db("db_stubs/test_connect_database_table_creation_copy.db", "test_table_creation.sql")
        self.assertTrue(filecmp.cmp(
            "test_table_creation.sql",
            "db_stubs/checks/test_table_creation_check.sql",
            shallow=False))
        #cleanup
        backend.conn.close()
        os.remove("db_stubs/test_connect_database_table_creation_copy.db")
        os.remove("test_table_creation.sql")

    #NOTE: Having tested connect_database(), the rest of the tests can use mocks to avoid adding more database stubs (where possible)

    def test_check_admin(self):
        backend.conn = MagicMock()
        backend.cur = MagicMock()
        backend.cur.fetchall = MagicMock( #mocking the call to the db that returns the admin credentials
            return_value =    
                [
                    ["arpit",
                    "123"]
                ]
        )
        self.assertTrue(backend.check_admin("arpit", "123"))
        self.assertIsNone(backend.check_admin("not_an_admin", "not_an_admin"))

    def test_create_employee(self):
        # copyfile(src="db_stubs/test_empty_db.db",
        #          dst="db_stubs/test_employee_insert.db")

        # backend.conn = sqlite3.connect("db_stubs/test_employee_insert.db")

        # self.assertTrue(filecmp.cmp(
        #     "db_stubs/test_create_employee.db",
        #     "db_stubs/test_create_employee_check.db"))
        pass

    def test_check_employee(self):
        pass

    def test_create_customer(self):
        pass

    def test_check_acc_no(self):
        pass

    def test_get_details(self):
        pass

    def test_update_balance(self):
        pass

    def test_deduct_balance(self):
        pass

    def test_check_balance(self):
        pass

    def test_update_name_in_bank_table(self):
        pass

    def test_update_age_in_bank_table(self):
        pass
    
    def test_update_address_in_bank_table(self):
        pass

    def test_list_all_customers(self):
        pass

    def test_delete_acc(self):
        pass

    def test_show_employees(self):
        pass

    def test_all_money(self):
        pass

    def test_show_employees_for_update(self):
        pass

    def test_update_employee_name(self):
        pass
    
    def test_update_employee_password(self):
        pass

    def test_update_employee_salary(self):
        pass

    def test_update_employee_position(self):
        pass

    def test_get_detail(self):
        pass

    def test_check_name_in_staff(self):
        pass


if __name__ == '__main__':
    unittest.main()