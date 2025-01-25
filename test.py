import mysql.connector
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="empmansys"
        )
        return connection
    except mysql.connector.Error as Err:
        print(f"error {Err}")
        return None
def Add_employee(cursor):
    emp_id=int(input(" enter the employee id \t"))
    emp_name=input("enter the employee name \t")
    emp_salary=int(input("enter the employees salary \t"))
    emp_dept=input("enter the employees dept \t")

    query="INSERT INTO employee VALUES(%s,%s,%s,%s)"
    VALUES=(emp_id,emp_name,emp_salary,emp_dept)
    cursor.execute(query,VALUES)
    print("employee added successfully")
def Update_employee(cursor):
    emp_id=int(input("enter the employee id you want to update \t"))
    print("Enter the detail to be updated \t")
    ch=int(input("1. NAME\t 2.SALARY\t 3.DEPT \t"))
    if ch==1:
        new_name=input("enter new name \t")
        query="UPDATE employee SET emp_name=%s where emp_id=%s"
        values=(new_name,emp_id)
        cursor.execute(query,values)
    if ch==2:
        new_salary=float(input("enter new salary \t"))
        query="UPDATE employee SET emp_salary=%s where emp_id=%s"
        values=(new_salary,emp_id)
        cursor.execute(query,values)
    if ch==3:
        new_dept=input("enter new dept \t")
        query="UPDATE employee SET emp_dept=%s where emp_id=%s"
        values=(new_dept,emp_id)
        cursor.execute(query,values)
def Delete_employee(cursor):
    emp_id=int(input("enter the employee id to be deleted \t"))
    query="DELETE FROM employee WHERE emp_id=%s"
    values=(emp_id,)
    cursor.execute(query,values)

def view_employee(cursor):
    query="SELECT * FROM employee"
    try:
        cursor.execute(query)
        results=cursor.fetchall()
        for item in results:
            print(f"ID: {item[0]}",end=" ")
            print(f"NAME: {item[1]}",end=" ")
            print(f"SALARY: {item[2]}",end=" ")
            print(f"DEPT: {item[3]}")
    except mysql.connector.Error as err:
        print(f"Error {err}")
def search_employee(cursor):
    print("ENTER HOW YOU WANT TO SEARCH \n")
    cho=int(input("1.by id  \n 2. by name"))
    if cho==1:

        emp_id=int(input("enter the employee id \t"))
        query="SELECT * from employee where emp_id=%s"
        values=(emp_id,)
        cursor.execute(query,values)
        results=cursor.fetchall()
        if not results:
            print("NO RECORDS FOUND")
        else:
            for item in results:
                print(f"ID: {item[0]}",end=" ")
                print(f"NAME: {item[1]}",end=" ")
                print(f"SALARY: {item[2]}",end=" ")
                print(f"DEPT: {item[3]}")

    elif cho==2:
        name=input("enter the name \t")
        query="select * from employee where emp_name like %s"
        values=(name,)
        cursor.execute(query,values)
        results=cursor.fetchall()
        if not results:
            print("NO RECORDS FOUND")
        else:
            for item in results:
                print(f"ID: {item[0]}",end=" ")
                print(f"NAME: {item[1]}",end=" ")
                print(f"SALARY: {item[2]}",end=" ")
                print(f"DEPT: {item[3]}")


def main():
    connection = connect_to_db()
    if not connection:
        print("failed")
        return 
    cursor = connection.cursor()
    while(True):
        print("\n\n EMPLOYEE MANAGEMENT SYSTEM")
        print("1.ADD EMPLOYEE")
        print("2.UPDATE EMPLOYEE")
        print("3.DELETE EMPLOYEE")
        print("4.VIEW EMPLOYEE")
        print("5.SEARCH EMPLOYEE")
        print("6.EXIT APPLICATION")

        choice=int(input("ENTER YOUR CHOICE: \t"))
        if choice==1:
            Add_employee(cursor)
            connection.commit()
        elif choice==2:
            Update_employee(cursor)
            connection.commit()

        elif choice==3:
            Delete_employee(cursor)
            connection.commit()

        elif choice==4:
            view_employee(cursor)

        elif choice==5:
            search_employee(cursor)

        elif choice==6:
            connection.commit()
            break
if __name__=="__main__":
    main()
