import unittest
import sqlite3
import os
from unittest.mock import patch, MagicMock
import backend
import filecmp
from dump_db import dump_db
from shutil import copyfile

#TODO: research stubs, mocks, fakes

#TODO: ask prof:
#                *testing with fors (mby paramaterized testing)
#                *if using current setup with db stubs is ok 
#                *if testing only backend would be enough

#TODO: ask abt the following:
#     *does testing that requires data (the database stubs) suddenly become integration testing instead of unit testing?
#      ANSWER: kind of, but it's not an issue for the project
#     *should unit tests instead test that the right method is called with the right params?
#      ANSWER: we will do both (depending on the effects of the function being tested)
# For doc: https://softwareengineering.stackexchange.com/questions/206539/unit-tests-and-databases-at-which-point-do-i-actually-connect-to-the-database
# https://stackoverflow.com/questions/145131/whats-the-best-strategy-for-unit-testing-database-driven-applications?rq=1
# https://stackoverflow.com/questions/71641581/approaches-for-unit-testing-db-components
# https://softwareengineering.stackexchange.com/questions/206539/unit-tests-and-databases-at-which-point-do-i-actually-connect-to-the-database

#NOTE: remember to keep each test entirely self-contained
#NOTE: functions that are explicitly supposed to modify the database will be tested using stubs
#      (in db_stubs subdirectory) since the actual thing being tested is the query 
#NOTE: the stub dbs in db_stubs shouldnt be worked with directly, but instead a copy should be made and worked with
#NOTE: The tests that have a dedicated "cleanup" section, have it placed after the assert call intentionally
#      if the test fails, it will not do the clean up, leaving the relevant files to be looked at to see what went wrong

#NOTE: steps to add a test that follows the Copy-Call-Dump-AssertWithCompare-Cleanup:
# 1. In File Explorer: Add a database stub file with the name of the test you re writing in the db_stubs folder (not in checks)
#    This database stubs should have the exact data needed by the function we re testing and no more
# 2. In the test: add the copyfile(src="name_of_test.db", dst="name_of_test_copy.db") so that the database stub you just
#    made with all the proper data needed by the function is not going to get changed
# 3. In the test: assign the proper varaibles to backend.conn and backend.cur (and any other global variables the function uses)
# 4. In the test: call dump_db("name_of_test_copy.db") to generate a dump of the db file the function we re testing just modified
#    This is necessary because we cant compare .db files but we can compare .sql dump files
# 5. In the test: add the assert: self.assertTrue(filecmp.cmp("name_of_test.sql", "db_stubs/checks/name_of_test_check.sql"))
# 6. In the test: add the cleanup: close the connection to the database, delete the copy database that s been modified by the
#    function we re testing and delete the .sql dump file we used to compare with our "check" .sql dump file
# 7: Run the tests with $python backend_unittests.py
# 8: The test you wrote will fail bcs there is no "check" .sql dump file
# 9. Add the not yet deleted "name_of_test.sql" dump file to the db_stubs/checks and rename it to have a trailing "_check"
# 10. Delete the "name_of_test_copy.db" from db_stubs
# 11. Run the tests again and it should work



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

    def test_connect_database_else(self):
        #make a copy of the stub
        copyfile(src="db_stubs/test_connect_database_else.db",
                 dst="db_stubs/test_connect_database_else_copy.db")

        backend.connect_database("db_stubs/test_connect_database_else_copy.db") #call the function

        backend.conn = sqlite3.connect("db_stubs/test_connect_database_else_copy.db")
        backend.cur = backend.conn.cursor()
        backend.cur.execute(
            "insert into bank values(?,?,?,?,?,?,?)",
            (1, "name", 1, "address", 1, "acc_type", 1),
        )
        backend.conn.commit()

        backend.connect_database("db_stubs/test_connect_database_else_copy.db") #call the function for the else branch
        self.assertEqual(backend.acc_no, 2)

        #cleanup
        backend.conn.close()
        os.remove("db_stubs/test_connect_database_else_copy.db")

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


    #3 teste pentru aceasta functie - 2 pentru if: caz in care numarul se afla in lista, caz in care nu se afla; unul pentru for - lista vida
    #test pentru if -- numar care se afla in lista
    def test_check_acc_no_if(self):
        # make a copy of the stub
        copyfile(src="db_stubs/test_check_acc_no_if.db",
                 dst="db_stubs/test_check_acc_no_if_copy.db")

        backend.connect_database("db_stubs/test_check_acc_no_if_copy.db")  # call the function


        result = backend.check_acc_no(1)
        self.assertTrue(result)

        # cleanup
        backend.conn.close()
        os.remove("db_stubs/test_check_acc_no_if_copy.db")

    def test_check_acc_no_if_else(self):
        # make a copy of the stub
        copyfile(src="db_stubs/test_check_acc_no_if.db",
                 dst="db_stubs/test_check_acc_no_if_else_copy.db")

        backend.connect_database("db_stubs/test_check_acc_no_if_else_copy.db")  # call the function

        result = backend.check_acc_no(5) #nu se afla in lista
        self.assertFalse(result)

        # cleanup
        backend.conn.close()
        os.remove("db_stubs/test_check_acc_no_if_else_copy.db")

    #lista vida
    def test_check_acc_no_for(self):
        # make a copy of the stub
        copyfile(src="db_stubs/test_check_acc_no_for.db",
                 dst="db_stubs/test_check_acc_no_for_copy.db")

        backend.connect_database("db_stubs/test_check_acc_no_for_copy.db")  # call the function

        result = backend.check_acc_no(1)
        self.assertFalse(result)

        # cleanup
        backend.conn.close()
        os.remove("db_stubs/test_check_acc_no_for_copy.db")

    #2 cazuri: pentru if- nu exista persoana cu acel acc_number, else - exista
    def test_get_details_if(self):
        # make a copy of the stub
        copyfile(src="db_stubs/test_get_details_if.db",
                 dst="db_stubs/test_get_details_if_copy.db")

        backend.connect_database("db_stubs/test_get_details_if_copy.db")  # call the function

        result = backend.check_acc_no(5) #nu exista persoana cu acest acc_number
        self.assertFalse(result)

        # cleanup
        backend.conn.close()
        os.remove("db_stubs/test_get_details_if_copy.db")

    def test_get_details_else(self):
        # make a copy of the stub
        copyfile(src="db_stubs/test_get_details_else.db",
                 dst="db_stubs/test_get_details_else_copy.db")

        backend.connect_database("db_stubs/test_get_details_else_copy.db")  # call the function

        backend.conn = sqlite3.connect("db_stubs/test_get_details_else_copy.db")
        backend.cur = backend.conn.cursor()
        value_to_insert = (1, "Popescu Ion", 28, "25th Street, NY", 100, "acc_type_1", 1)
        backend.cur.execute(
            "insert into bank values(?,?,?,?,?,?,?)",
            (1, "Popescu Ion", 28, "25th Street, NY", 100, "acc_type_1", 1),
        )
        backend.conn.commit()
        backend.conn.close()

        backend.connect_database("db_stubs/test_get_details_else_copy.db")  # call the function
        result = backend.get_details(acc_no=1)
        self.assertEqual(result, value_to_insert)


        # cleanup
        backend.conn.close()
        os.remove("db_stubs/test_get_details_else_copy.db")

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
        copyfile(src="db_stubs/test_check_balance.db",
                 dst="db_stubs/test_check_balance_copy.db")

        #hardcoded result, no query
        result_from_db = 10000

        backend.connect_database("db_stubs/test_check_balance_copy.db")  # call the function
        backend.cur = backend.conn.cursor()
        result = backend.check_balance(acc_no=1)

        self.assertEqual(result,result_from_db)

        # cleanup
        backend.conn.close()
        os.remove("db_stubs/test_check_balance_copy.db")

    def test_update_name_in_bank_table(self):
        copyfile(src="db_stubs/test_update_name_in_bank_table.db",
                    dst="db_stubs/test_update_name_in_bank_table_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_update_name_in_bank_table_copy.db")
        backend.cur = backend.conn.cursor()
        backend.update_name_in_bank_table(new_name="new_name", acc_no=1)
        
        dump_db("db_stubs/test_update_name_in_bank_table_copy.db", "test_update_name_in_bank_table.sql")

        self.assertTrue(filecmp.cmp(
            "test_update_name_in_bank_table.sql",
            "db_stubs/checks/test_update_name_in_bank_table_check.sql"))
        
        #cleanup
        backend.conn.close()
        os.remove("test_update_name_in_bank_table.sql")
        os.remove("db_stubs/test_update_name_in_bank_table_copy.db")

    def test_update_age_in_bank_table(self):
        copyfile(src="db_stubs/test_update_age_in_bank_table.db",
                 dst="db_stubs/test_update_age_in_bank_table_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_update_age_in_bank_table_copy.db")
        backend.cur = backend.conn.cursor()
        backend.update_age_in_bank_table(new_name=39,acc_no=2)

        dump_db("db_stubs/test_update_age_in_bank_table_copy.db", "test_update_age_in_bank_table.sql")

        self.assertTrue(filecmp.cmp(
            "test_update_age_in_bank_table.sql",
            "db_stubs/checks/test_update_age_in_bank_table_check.sql"))

        # cleanup
        backend.conn.close()
        os.remove("test_update_age_in_bank_table.sql")
        os.remove("db_stubs/test_update_age_in_bank_table_copy.db")
    
    def test_update_address_in_bank_table(self):
        copyfile(src="db_stubs/test_update_address_in_bank_table.db",
                 dst="db_stubs/test_update_address_in_bank_table_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_update_address_in_bank_table_copy.db")
        backend.cur = backend.conn.cursor()
        backend.update_address_in_bank_table(new_name="Calea Mosilor 22", acc_no=2)

        dump_db("db_stubs/test_update_address_in_bank_table_copy.db", "test_update_address_in_bank_table.sql")

        self.assertTrue(filecmp.cmp(
            "test_update_address_in_bank_table.sql",
            "db_stubs/checks/test_update_address_in_bank_table_check.sql"))

        # cleanup
        backend.conn.close()
        os.remove("test_update_address_in_bank_table.sql")
        os.remove("db_stubs/test_update_address_in_bank_table_copy.db")

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
        copyfile(src="db_stubs/test_update_employee_name.db",
                 dst="db_stubs/test_update_employee_name_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_update_employee_name_copy.db")
        backend.cur = backend.conn.cursor()
        backend.update_employee_name(new_name="Ionescu Mirela-Oana", old_name="Ionescu Mirela")

        dump_db("db_stubs/test_update_employee_name_copy.db", "test_update_employee_name.sql")

        self.assertTrue(filecmp.cmp(
            "test_update_employee_name.sql",
            "db_stubs/checks/test_update_employee_name_check.sql"))

        # cleanup
        backend.conn.close()
        os.remove("test_update_employee_name.sql")
        os.remove("db_stubs/test_update_employee_name_copy.db")
    
    def test_update_employee_password(self):
        copyfile(src="db_stubs/test_update_employee_password.db",
                 dst="db_stubs/test_update_employee_password_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_update_employee_password_copy.db")
        backend.cur = backend.conn.cursor()
        backend.update_employee_password(new_pass="newpassword", old_name="Ionescu Mirela")

        dump_db("db_stubs/test_update_employee_password_copy.db", "test_update_employee_password.sql")

        self.assertTrue(filecmp.cmp(
            "test_update_employee_password.sql",
            "db_stubs/checks/test_update_employee_password_check.sql"))

        # cleanup
        backend.conn.close()
        os.remove("test_update_employee_password.sql")
        os.remove("db_stubs/test_update_employee_password_copy.db")

    def test_update_employee_salary(self):
        copyfile(src="db_stubs/test_update_employee_salary.db",
                 dst="db_stubs/test_update_employee_salary_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_update_employee_salary_copy.db")
        backend.cur = backend.conn.cursor()
        backend.update_employee_salary(new_salary=3000, old_name="Ionescu Mirela")

        dump_db("db_stubs/test_update_employee_salary_copy.db", "test_update_employee_salary.sql")

        self.assertTrue(filecmp.cmp(
            "test_update_employee_salary.sql",
            "db_stubs/checks/test_update_employee_salary_check.sql"))

        # cleanup
        backend.conn.close()
        os.remove("test_update_employee_salary.sql")
        os.remove("db_stubs/test_update_employee_salary_copy.db")

    def test_update_employee_position(self):
        copyfile(src="db_stubs/test_update_employee_position.db",
                 dst="db_stubs/test_update_employee_position_copy.db")

        backend.conn = sqlite3.connect("db_stubs/test_update_employee_position_copy.db")
        backend.cur = backend.conn.cursor()
        backend.update_employee_position(new_pos="manager",old_name="Popescu Maria")

        dump_db("db_stubs/test_update_employee_position_copy.db", "test_update_employee_position.sql")

        self.assertTrue(filecmp.cmp(
            "test_update_employee_position.sql",
            "db_stubs/checks/test_update_employee_position_check.sql"))

        # cleanup
        backend.conn.close()
        os.remove("test_update_employee_position.sql")
        os.remove("db_stubs/test_update_employee_position_copy.db")

    def test_get_detail(self):
        # make a copy of the stub
        copyfile(src="db_stubs/test_check_get_detail.db",
                 dst="db_stubs/test_check_get_detail_copy.db")

        #result from db, no query
        result_from_db = [("Lungu Elena", 10000)]

        backend.connect_database("db_stubs/test_check_get_detail_copy.db")  # call the function

        result = backend.get_detail(acc_no=1)
        self.assertEqual(result,result_from_db)

        # cleanup
        backend.conn.close()
        os.remove("db_stubs/test_check_get_detail_copy.db")

    #cazul in care numele se afla in lista
    def test_check_name_in_staff_if(self):
        # make a copy of the stub
        copyfile(src="db_stubs/test_check_name_in_staff_if.db",
                 dst="db_stubs/test_check_name_in_staff_if_copy.db")

        backend.connect_database("db_stubs/test_check_name_in_staff_if_copy.db")  # call the function

        result = backend.check_name_in_staff("Ionescu Mirela")
        self.assertTrue(result)

        # cleanup
        backend.conn.close()
        os.remove("db_stubs/test_check_name_in_staff_if_copy.db")

    #cazul in care numele nu exista in lista
    def test_check_name_in_staff_else(self):
        # make a copy of the stub
        copyfile(src="db_stubs/test_check_name_in_staff_else.db",
                 dst="db_stubs/test_check_name_in_staff_else_copy.db")

        backend.connect_database("db_stubs/test_check_name_in_staff_else_copy.db")  # call the function

        result = backend.check_name_in_staff("Rusu Mihai")
        self.assertFalse(result)

        # cleanup
        backend.conn.close()
        os.remove("db_stubs/test_check_name_in_staff_else_copy.db")

    #cazul in care avem lista vida
    def test_check_name_in_staff_for(self):
        # make a copy of the stub
        copyfile(src="db_stubs/test_check_name_in_staff_for.db",
                 dst="db_stubs/test_check_name_in_staff_for_copy.db")

        backend.connect_database("db_stubs/test_check_name_in_staff_for_copy.db")  # call the function

        result = backend.check_name_in_staff("Rusu Mihai")
        self.assertFalse(result)

        # cleanup
        backend.conn.close()
        os.remove("db_stubs/test_check_name_in_staff_for_copy.db")






if __name__ == '__main__':
    unittest.main()