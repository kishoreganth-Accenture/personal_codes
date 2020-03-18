import os
import datetime

"""
Class to check table exists and do create or insert operation
"""
class CreateInsert:
    def __init__(self, logger, db):
        self.logger = logger
        self.db = db
        self.cursor = db.cursor()

    # method to check the tables is present or not and empty or not
    def check_table(self, name):
        """
        :param name: table_name
        :return: table data
        """
        self.cursor.execute("use datamodel")
        self.db.commit()
        self.cursor.execute("show tables")
        self.logger.info("Tables are fetched from database")
        table = self.cursor.fetchall()
        # flag = 0

        try:
            for tables in table:
                if name in tables:
                    # flag = 1
                    self.cursor.execute("select * from {}".format(name))
                    data = self.cursor.fetchall()
                    data_len = len(data)
                    if data_len == 0:
                        return 'insert'
                    else:
                        self.cursor.execute('select * from {}'.format(name))
                        result_set = self.cursor.fetchall()
                        return result_set
            else:
                return 'create'

        except Exception as e:
            print(e)
            self.logger.exception("Exception occured!!!!!")

    # Method to fetch the ddl path
    def path_ddl(self,path ="ddl"):
        try:
            ddl_folder = os.path.dirname(os.path.dirname(__file__))
            ddl_path = ddl_folder + "\\" + '{}'.format("ddl")
            if ddl_path != ddl_folder + "\\" + '{}'.format(path):
                raise Exception
            self.logger.info("Path of the ddl folder is fetched : {}".format(ddl_path))
            # print(ddl_path)
            return ddl_path

        except Exception as e:
            return "path not found"
            self.logger.exception("Exception occured!!!!!")

    # Method to create table
    def create_table(self, name):
        """
            Parameter : name of file
            Return : nothing
        """
        ddl_path = self.path_ddl()
        try:
            file_open = open(ddl_path + '\\' + '{}.sql'.format(name))
            lines = file_open.read().split(';')
            create = lines[0].strip()
            self.cursor.execute(create)
            self.db.commit()
            self.logger.info("Table {} is created ".format(name))
            self.insert_table(name)  # insert_table method is invoked for inserting the data's
            file_open.close()
            return name

        except FileNotFoundError as e:
            return "file not found"
            self.logger.exception("File not found")

    # Method to insert values into table
    def insert_table(self, name):
        """
            Parameter : name of file
            Return : records of the table
        """

        ddl_path = self.path_ddl()  # function call to fetch ddl dir path
        try:
            self.cursor.execute("select column_name from information_schema.columns where table_schema='datamodel' and "
                                "table_name='{}' order by ordinal_position".format(name))
            col_names = self.cursor.fetchall()
            nested_list = [list(x) for x in col_names]
            flat_list = [item for sublist in nested_list for item in sublist]

            if '_expected' in name:
                e_name = name.replace('_expected', '')
                file = open(ddl_path + '\\' + '{}.csv'.format(e_name))
                # splitted = name.split(',')
                # self.cursor.execute("insert into {} ({}) values({})".format(splitted.pop(0),splitted, ), val_list)

            else:
                file = open(ddl_path + '\\' + '{}.csv'.format(name))
            value = file.read().splitlines()
            for val in value:
                val_list = val.split(",")
                val_list.append(datetime.datetime.now())
                keys = (",".join(flat_list))
                joiner = (",".join(["%s" for x in range(len(val_list))]))
                self.cursor.execute("insert into {} ({}) values({})".format(name, keys, joiner), val_list)
            self.db.commit()
            self.logger.info("Data's are inserted into table {}".format(name))
            self.cursor.execute('select * from {}'.format(name))
            result_set = self.cursor.fetchall()
            file.close()
            return result_set

        except Exception as e:
            return "exception"
            self.logger.exception("Exception occurred!!!!!")
