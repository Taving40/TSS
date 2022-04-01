import unittest
import sqlite3
import os
from unittest.mock import patch, MagicMock
import backend
import filecmp
from dump_db import dump_db
from shutil import copyfile

#TODO: ask abt the following:
#     *does testing that requires data (the database stubs) suddenly become integration testing instead of unit testing?
#     *should unit tests instead test that the right method is called with the right params?
# Pretty sure the second answer from this thread says that the way Im doing it is right: https://softwareengineering.stackexchange.com/questions/206539/unit-tests-and-databases-at-which-point-do-i-actually-connect-to-the-database
# Hopefully prof agrees

#Links: https://stackoverflow.com/questions/145131/whats-the-best-strategy-for-unit-testing-database-driven-applications?rq=1
# https://stackoverflow.com/questions/71641581/approaches-for-unit-testing-db-components
# https://softwareengineering.stackexchange.com/questions/206539/unit-tests-and-databases-at-which-point-do-i-actually-connect-to-the-database

#NOTE: remember to keep each test entirely self-contained
#NOTE: functions that are explicitly supposed to modify the database will be tested using stubs
#      (in db_stubs subdirectory) since the actual thing being tested is the query 
#NOTE: the stub dbs in db_stubs shouldnt be worked with directly, but instead a copy should be made and worked with
#NOTE: The tests that have a dedicated "cleanup" section, have it placed after the assert call intentionally
#      if the test fails, it will not do the clean up, leaving the relevant files to be looked at to see what went wrong

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

    def test_check_admin_true(self):
        backend.conn = MagicMock()
        backend.cur = MagicMock()
        backend.cur.fetchall = MagicMock( #mocking the call to the db that returns the admin credentials
            return_value =    
                [
                    ["admin",
                    "password"]
                ]
        )
        self.assertTrue(backend.check_admin("admin", "password"))

    def test_check_admin_wrong_pass(self):
        backend.conn = MagicMock()
        backend.cur = MagicMock()
        backend.cur.fetchall = MagicMock( #mocking the call to the db that returns the admin credentials
            return_value =    
                [
                    ["admin",
                    "password"]
                ]
        )
        self.assertIsNone(backend.check_admin("admin", "incorrect_password"))

    def test_check_admin_wrong_user(self):
        backend.conn = MagicMock()
        backend.cur = MagicMock()
        backend.cur.fetchall = MagicMock( #mocking the call to the db that returns the admin credentials
            return_value =    
                [
                    ["admin",
                    "password"]
                ]
        )
        self.assertIsNone(backend.check_admin("incorrect_admin", "password"))

    def test_create_employee(self):
        copyfile(src="db_stubs/test_create_employee.db",
                 dst="db_stubs/test_create_employee_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_create_employee_copy.db")
        backend.cur = backend.conn.cursor()
        backend.create_employee(name="name", password="password", salary=1, position="position")
        
        dump_db("db_stubs/test_create_employee_copy.db", "test_create_employee.sql")

        self.assertTrue(filecmp.cmp(
            "test_create_employee.sql",
            "db_stubs/checks/test_create_employee_check.sql"))
        
        #cleanup
        backend.conn.close()
        os.remove("test_create_employee.sql")
        os.remove("db_stubs/test_create_employee_copy.db")

    def test_check_employee_true(self):
        backend.conn = MagicMock()
        backend.cur = MagicMock()
        backend.cur.fetchall = MagicMock( #mocking the call to the db that returns the admin credentials
            return_value =    
                [
                    ["employee1",
                    "password1"],
                    ["employee2",
                    "password2"]
                ]
        )
        self.assertTrue(backend.check_employee("employee1", "password1"))

    def test_check_employee_wrong_pass(self):
        backend.conn = MagicMock()
        backend.cur = MagicMock()
        backend.cur.fetchall = MagicMock( #mocking the call to the db that returns the admin credentials
            return_value =    
                [
                    ["employee1",
                    "password1"],
                    ["employee2",
                    "password2"]
                ]
        )
        self.assertFalse(backend.check_employee("employee1", "password3"))
    
    def test_check_employee_wrong_user(self):
        backend.conn = MagicMock()
        backend.cur = MagicMock()
        backend.cur.fetchall = MagicMock( #mocking the call to the db that returns the admin credentials
            return_value =    
                [
                    ["employee1",
                    "password1"],
                    ["employee2",
                    "password2"]
                ]
        )
        self.assertFalse(backend.check_employee("employee3", "password1"))

    def test_create_customer(self):
        copyfile(src="db_stubs/test_create_customer.db",
                 dst="db_stubs/test_create_customer_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_create_customer_copy.db")
        backend.cur = backend.conn.cursor()
        backend.acc_no = 1
        backend.create_customer(name="name", age=1, address="address", balance=1, acc_type="acc_type", mobile_number=1)
        
        dump_db("db_stubs/test_create_customer_copy.db", "test_create_customer.sql")

        self.assertTrue(filecmp.cmp(
            "test_create_customer.sql",
            "db_stubs/checks/test_create_customer_check.sql"))
        
        #cleanup
        backend.conn.close()
        os.remove("test_create_customer.sql")
        os.remove("db_stubs/test_create_customer_copy.db")

    def test_check_acc_no(self):
        pass

    def test_get_details(self):
        pass

    def test_update_balance(self):
        copyfile(src="db_stubs/test_update_balance.db",
                 dst="db_stubs/test_update_balance_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_update_balance_copy.db")
        backend.cur = backend.conn.cursor()
        backend.update_balance(new_money=2, acc_no=1)
        
        dump_db("db_stubs/test_update_balance_copy.db", "test_update_balance.sql")

        self.assertTrue(filecmp.cmp(
            "test_update_balance.sql",
            "db_stubs/checks/test_update_balance_check.sql"))
        
        #cleanup
        backend.conn.close()
        os.remove("test_update_balance.sql")
        os.remove("db_stubs/test_update_balance_copy.db")

    def test_deduct_balance(self):
        copyfile(src="db_stubs/test_update_balance.db",
                 dst="db_stubs/test_update_balance_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_update_balance_copy.db")
        backend.cur = backend.conn.cursor()
        backend.update_balance(new_money=2, acc_no=1)
        
        dump_db("db_stubs/test_update_balance_copy.db", "test_update_balance.sql")

        self.assertTrue(filecmp.cmp(
            "test_update_balance.sql",
            "db_stubs/checks/test_update_balance_check.sql"))
        
        #cleanup
        backend.conn.close()
        os.remove("test_update_balance.sql")
        os.remove("db_stubs/test_update_balance_copy.db")

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