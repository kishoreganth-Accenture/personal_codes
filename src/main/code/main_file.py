import create_insert
import sys
import dml
import os

sys.path.insert(1, os.path.dirname(os.getcwd()) + '\\config')
import devconfig
import mysql.connector

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__)) + '\\' + 'logs')
import file_logs

"""
Main program to create,insert records in tables and do fetch
"""

files = ['student', 'city', 'class_detail', 'student_detail', 'class', 'mar'
                                                                       'ks']
log_files = ['student_log', 'city_log', 'class_detail_log', 'student_detail_log', 'class_log', 'marks_log']


# main() function calls the connection, creation and operation.
def main():
    env = sys.argv[1]
    loggers, db, cursor,database = connection(env)
    creation(loggers, db)
    operation_crud(loggers,cursor,database)
    operation(loggers, db, cursor,database)
    close(loggers, db)



# connection() to connect the db
def connection(env):
    """
    :param env: dev,int - user input
    :return: db cursor, log object
    """
    loggers = file_logs.logs_handler("connection_log", __name__)
    host, user, password, database = devconfig.connect_db(env)
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, db=database)
    except Exception as e:
        print(e)
    cursor = mydb.cursor()
    loggers.info("Database Connection Established {}@{} with password {}".format(user, host, '*' * len(password)))
    return loggers, mydb, cursor,database


def creation(loggers, db):
    """
    :param loggers: log object
    :param db: db connection
    """
    loggers.info("Object Created")
    for i in range(len(files)):
        if table_name == files[i]:
            loggers = file_logs.logs_handler(log_files[i], files[i])
            obj = create_insert.CreateInsert(loggers, db)
            option = obj.check_table(files[i])
            if option == 'create':
                obj.create_table(files[i])
            elif option == 'insert':
                obj.insert_table(files[i])
            else:
                print("Table ", "\"", files[i], "\"", " already exists with data")

def operation_crud(loggers,cursor,database):

    choice = input("Do you want to insert / update / select the table: ")
    if choice.strip().lower() == "select":
        cursor.execute("select * from {}".format(table_name))
        records = cursor.fetchall()
        for i in records:
                print(i)
    elif choice.strip().lower() == "update":
        try:
            cursor.execute("select column_name from information_schema.columns where table_name = '{}' and table_schema = '{}'".format(table_name,database))
            print([list(i) for i in cursor.fetchall()])
            u_column_name = input("which Column you want to change : ")
            u_column_value = input(" new {} : ".format(u_column_name))
            u_based_column = input(" based on what column (where) : ")
            u_based_value = int(input("enter the {} : ".format(u_based_column)))
            cursor.execute("update {} set {} = '{}' where {} ='{}'".format(table_name,u_column_name.strip().lower(),u_column_value.strip().lower(),u_based_column.strip().lower(),u_based_value))
            cursor.execute("select * from {}".format(table_name))
            print(cursor.fetchall())
        except Exception as e:
            print(e)
            loggers.exception(e)


def operation(loggers, db, cursor, database):
    """
    :param loggers: log object
    :param db: db conncetion
    :param cursor: cursor object
    """


    cursor.execute("use {}".format(database))
    cursor.execute("show tables")
    tables_in_sql = cursor.fetchall()
    tab_in_sql = []
    for tables in tables_in_sql:
        for table in tables:
            tab_in_sql.append(table)

    table_required = list(set(files) - set(tab_in_sql))
    if len(table_required) > 0:
        print(" Tables are insufficient to perform operation. ", (",").join(table_required), " - table is missing")
    else:
        dml_obj = dml.StudentDetails(db, cursor)
        loggers.info("Instance created for Dml operation")
        student_name = input("Enter the student name : ")
        class_no = input("Enter the class (10th/11th/12th) : ")
        dml_obj.total_marks_obtained(student_name, class_no)


def close(loggers, db):
    """
    :param loggers: log object
    :param db: db connection
    :return: close connection
    """
    try:
        db.close()
        loggers.info("Program ended And connection closed")
    except Exception as e:
        loggers.exception("Cant close the connection")


if __name__ == '__main__':
    table_name = sys.argv[2]
    main()
