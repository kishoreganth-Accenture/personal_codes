import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd()) + '\\config')
import devconfig
sys.path.insert(1, os.path.dirname(os.path.dirname(__file__)) + '\\' + 'logs')
import file_logs

"""
Class studentDetials to perform operations 
"""
class StudentDetails:
    def __init__(self, db, cursor):
        self.logger = file_logs.logs_handler("dml_log", "dml_log")
        self.db = db
        self.cursor = cursor

    def total_marks_obtained(self, student_name, class_no):

        self.cursor.execute(
            "select maths, physics, chemistry, biology, computer, english,"
            "case when maths>=50 then 'Pass' else 'Fail' end as maths1,"
            "case when physics>=50 then 'Pass' else 'Fail' end as physics1,"
            "case when chemistry>=50 then 'Pass' else 'Fail' end as chemistry1,"
            "case when biology>=50 then 'Pass' else 'Fail' end as biology1,"
            "case when computer>=50 then 'Pass' else 'Fail' end as computer1,"
            "case when english>=50 then 'Pass' else 'Fail' end as english1 "
            "from student s join marks m on s.id=m.id "
            "join class c on c.class_id=m.class_id "
            "where s.name='{}' and c.class='{}'"
            "group by s.id;".format(student_name, class_no))

        marks1 = self.cursor.fetchall()
        for mark in marks1:
            print("Maths     : ", mark[0], "-", mark[6])
            print("Physics   : ", mark[1], "-", mark[7])
            print("Chemistry : ", mark[2], "-", mark[8])
            print("Biology   : ", mark[3], "-", mark[9])
            print("Computer  : ", mark[4], "-", mark[10])
            print("English   : ", mark[5], "-", mark[11])
        self.logger.info("Marks of each subject of the student {} is found".format(student_name))

        self.cursor.execute(
            "select distinct (maths+biology+chemistry+english+physics+computer) as sum, "
            "((maths+biology+chemistry+english+physics+computer)/600)*100 as percentage "
            "from student s join marks m on s.id=m.id "
            "join class c on c.class_id=m.class_id "
            "where s.name='{}' and c.class='{}';".format(student_name, class_no))

        marks = self.cursor.fetchall()
        for mark in marks:
            print("Marks obtained out of 600 : ", mark[0])
            print("Percentage of marks obtained : ", mark[1])
        self.logger.info("Sum and Percentage of the student {} is found".format(student_name))

        self.cursor.execute(
            "select * from "
            "(select distinct name, "
            "dense_rank() over(partition by m.class_id "
            "order by maths+biology+chemistry+english+physics+computer desc) as std_rank, "
            "c.class from student s join marks m on s.id=m.id "
            "join class c on c.class_id=m.class_id) as tab "
            "where name = '{}' and class = '{}'".format(student_name, class_no))

        ranks = self.cursor.fetchall()
        for rank in ranks:
            print("Rank obtained is : ", rank[1])
            self.logger.info("Rank of the student {} from class {} and rank {} is found".format(student_name, class_no, rank[1]))
            return rank[1]
        else:
            return "no rank"
