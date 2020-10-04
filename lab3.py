import sqlite3
import pandas as pd


# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database

class DBOperations:
    sql_create_table_firsttime = "CREATE TABLE IF NOT EXISTS employee (" \
                                 "employee_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                                 "Title VARCHAR(4) NOT NULL, " \
                                 "Forename VARCHAR(20) NOT NULL, " \
                                 "Surname VARCHAR(20) NOT NULL, " \
                                 "EmailAddress VARCHAR (255) NOT NULL, " \
                                 "Salary FLOAT(20) NOT NULL" \
                                 ")"

    sql_create_table = "CREATE TABLE IF NOT EXISTS employee (" \
                       "employee_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                       "Title VARCHAR(4) NOT NULL, " \
                       "Forename VARCHAR(20) NOT NULL, " \
                       "Surname VARCHAR(20) NOT NULL, " \
                       "EmailAddress VARCHAR (255) NOT NULL, " \
                       "Salary FLOAT(20) NOT NULL" \
                       ")"

    sql_check_table_exists = "SELECT COUNT(*) " \
                             "FROM sqlite_master " \
                             "WHERE name = 'employee'"
    sql_insert = "INSERT INTO employee (Title, Forename, Surname, EmailAddress, Salary)" \
                 "VALUES(?, ?, ?, ?, ?);"
    sql_select_all = "SELECT * FROM employee"
    sql_search = "SELECT * " \
                 "FROM employee " \
                 "WHERE employee_id = ?;"
    sql_update_data = "UPDATE employee SET Forename=?, Surname=?, EmailAddress=?, Salary=? WHERE employee_id=?"
    sql_delete_data = "DELETE FROM employee WHERE employee_id=?"
    sql_drop_table = "DROP TABLE employee"

    def __init__(self):
        try:
            self.conn = sqlite3.connect("abcDB")
            self.cur = self.conn.cursor()
            # self.cur.execute(self.sql_create_table_firsttime)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def get_connection(self):
        self.conn = sqlite3.connect("abcDB")
        self.cur = self.conn.cursor()

    def create_table(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_check_table_exists)
            if self.cur.fetchone()[0] == 1:
                print("Table employee already exists")
            else:
                self.cur.execute(self.sql_create_table)
                self.conn.commit()
                print("Table created successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def drop_table(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_drop_table)
            self.conn.commit()
            print("Table dropped")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def insert_data(self):
        try:
            self.get_connection()

            emp = Employee()
            emp.set_employee_title(str(input("Enter Employee Title: ")))
            emp.set_forename(str(input("Enter Employee Forename: ")))
            emp.set_surname(str(input("Enter Employee Surname: ")))
            emp.set_email(str(input("Enter Employee Email: ")))
            emp.set_salary(float(input("Enter Employee Salary: ")))

            self.cur.execute(self.sql_insert, tuple(str(emp).split("\n")))
            self.conn.commit()
            last_row_id = self.cur.lastrowid
            print(last_row_id)
            print("Inserted data successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def select_all(self):
        try:
            self.get_connection()
            data = pd.read_sql_query(self.sql_select_all, self.conn)
            if data.empty:
                print('Table employee is empty!')
            else:
                print(data.to_string(index=False))
            # think how you could develop this method to show the records
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def search_data(self):
        try:
            self.get_connection()
            employee_id = int(input("Enter Employee ID: "))
            self.cur.execute(self.sql_search, tuple(str(employee_id)))
            result = self.cur.fetchone()
            if type(result) == type(tuple()):
                for index, detail in enumerate(result):
                    if index == 0:
                        print("Employee ID: " + str(detail))
                    elif index == 1:
                        print("Employee Title: " + detail)
                    elif index == 2:
                        print("Employee Name: " + detail)
                    elif index == 3:
                        print("Employee Surname: " + detail)
                    elif index == 4:
                        print("Employee Email: " + detail)
                    else:
                        print("Salary: " + str(detail))
            else:
                print("No Record")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def update_data(self):
        try:
            self.get_connection()
            # Update statement
            employee_id = int(input("Enter Employee ID: "))
            forename = str(input("Enter Employee Forename: "))
            surname = str(input("Enter Employee Forename: "))
            email_address = str(input("Enter Employee Forename: "))
            salary = str(input("Enter Employee Forename: "))
            result = self.cur.execute(self.sql_update_data, ((str(forename)), (str(surname)), (str(email_address)), (float(salary), (str(employee_id)))))
            if result.rowcount != 0:
                print(str(result.rowcount) + "Row(s) affected.")
            else:
                print("Cannot find this record in the database")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # Define Delete_data method to delete data from the table.
    # The user will need to input the employee id to delete the corrosponding record.
    def delete_data(self):
        try:
            self.get_connection()
            employee_id = int(input("Enter Employee ID: "))
            result = self.cur.execute(self.sql_delete_data, tuple(str(employee_id)))
            if result.rowcount != 0:
                self.conn.commit()
                print(str(result.rowcount) + "Row(s) affected.")
            else:
                print("Cannot find this record in the database")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()


class Employee:

    def __init__(self):
        self.employee_id = 0
        self.empTitle = ''
        self.forename = ''
        self.surname = ''
        self.email = ''
        self.salary = 0.0

    def set_employee_id(self, employee_id):
        self.employee_id = employee_id

    def set_employee_title(self, emp_title):
        self.empTitle = emp_title

    def set_forename(self, forename):
        self.forename = forename

    def set_surname(self, surname):
        self.surname = surname

    def set_email(self, email):
        self.email = email

    def set_salary(self, salary):
        self.salary = salary

    def get_employee_id(self):
        return self.employee_id

    def get_employee_title(self):
        return self.empTitle

    def get_forename(self):
        return self.forename

    def get_surname(self):
        return self.surname

    def get_email(self):
        return self.email

    def get_salary(self):
        return self.salary

    def __str__(self):
        # str(self.employee_id) + "\n" +
        return self.empTitle + "\n" + self.forename + "\n" + self.surname + "\n" + self.email + "\n" + str(self.salary)


# The main function will parse arguments.
# These argument will be defined by the users on the console.
# The user will select a choice from the menu to interact with the database.

while True:
    print("\n Menu:")
    print("**********")
    print(" 1. Create table EmployeeUoB")
    print(" 2. Insert data into EmployeeUoB")
    print(" 3. Select all data into EmployeeUoB")
    print(" 4. Search an employee")
    print(" 5. Update data some records")
    print(" 6. Delete data some records")
    print(" 7. Drop table Employee")
    print(" 8. Exit\n")

    __choose_menu = int(input("Enter your choice: "))
    db_ops = DBOperations()
    if __choose_menu == 1:
        db_ops.create_table()
    elif __choose_menu == 2:
        db_ops.insert_data()
    elif __choose_menu == 3:
        db_ops.select_all()
    elif __choose_menu == 4:
        db_ops.search_data()
    elif __choose_menu == 5:
        db_ops.update_data()
    elif __choose_menu == 6:
        db_ops.delete_data()
    elif __choose_menu == 7:
        db_ops.drop_table()
    elif __choose_menu == 8:
        exit(0)
    else:
        print("Invalid Choice")
