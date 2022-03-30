from backend import *
import unittest
import sqlite3
import os

#NOTE: remember to keep each test entirely self-contained (dont)

class BackendUnitTests(unittest.TestCase):

    #test that the global connection object is initialized properly
    def test_connect_database_connection(self):
        connect_database("db_stubs/test_empty.db") #call the function
        from backend import conn #reimport the global conn value to access the newly modified value
        self.assertIsInstance(conn, sqlite3.Connection) #check if it is the appropriate class

    #test that the global cursor object for the connection is initialized properly
    def test_connect_database_cursor(self):
        connect_database("db_stubs/test_empty.db")
        from backend import cur
        self.assertIsInstance(cur, sqlite3.Cursor)

    #test that the global account number object is initialized properly
    def test_connect_database_account_number(self): 
        connect_database("db_stubs/test_empty.db")
        from backend import acc_no
        self.assertIsInstance(acc_no, int)

    #test that the global account number object has proper value
    def test_connect_database_account_number(self): 
        connect_database("db_stubs/test_empty.db")
        from backend import acc_no
        self.assertGreater(acc_no, 0)

    #test that all the tables were created
    def test_connect_database_table_creation(self):
        #remove the stub if it exists for consistency
        if os.path.exists("db_stubs/test_table_creation.db"):
            os.remove("db_stubs/test_table_creation.db")

        #call the function 
        connect_database("db_stubs/test_table_creation.db")

        #get the names of the tables that have been created in the stub
        def check_table_names():
            conn = sqlite3.connect("db_stubs/test_table_creation.db")
            cur = conn.cursor()
            query = """SELECT name FROM sqlite_master 
                        WHERE type='table';"""
            cur.execute(query)
            tables = [ 
                v[0] for v in cur.fetchall()
                if v[0] != "sqlite_sequence"
            ]
            return tables
        
        #check the names are equal to the intended ones
        self.assertSetEqual(set(check_table_names()),
                            set(["bank", "staff", "admin"]))



    def test_check_admin(self):
        pass

    def test_create_employee(self):
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