from prettytable import PrettyTable
from collections import defaultdict
import unittest
import sqlite3


class Student:
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course_map = dict()

    def add_grade(self, course_name, grade):
        self.course_map[course_name] = grade

    def generate_student_summary(self):
        passed = list()
        for course, grade in self.course_map.items():
            if grade != 'F':
                passed.append(course)
        return_list = [self.cwid, self.name, self.major, sorted(passed)]
        return return_list


class Instructor:
    def __init__(self, cwid, name, department):
        self.cwid = cwid
        self.name = name
        self.department = department
        self.course_map = defaultdict(int)

    def add_student(self, course_name):
        self.course_map[course_name] += 1

    def generate_instructor_summary(self):
        return_list = list()
        for course_name, student_amount in self.course_map.items():
            return_list.append([self.cwid, self.name, self.department, course_name, student_amount])
        return return_list


class University:
    def __init__(self):
        self.student_list = dict()
        self.instructor_list = dict()
        self.major_list = defaultdict(lambda: defaultdict(set))

    def get_student_info(self, file_path):
        file = self.file_reader(file_path)
        for line in file:
            student = Student(line[0], line[1], line[2])
            self.student_list[line[0]] = student

    def get_instructor_info(self, file_path):
        file = self.file_reader(file_path)
        for line in file:
            instructor = Instructor(line[0], line[1], line[2])
            self.instructor_list[line[0]] = instructor

    def get_grade_info(self, file_path):
        file = self.file_reader(file_path)
        for line in file:
            self.student_list[line[0]].add_grade(line[1], line[2])
            self.instructor_list[line[3]].add_student(line[1])

    def get_major_info(self,file_path):
        file = self.file_reader(file_path)
        for line in file:
            self.major_list[line[0]][line[1]].add(line[2])

    def file_reader(self, file_path):
        try:
            file = open(file_path)
        except FileNotFoundError:
            raise FileNotFoundError("Can't find and open the file")
        with file:
            return_list = list()
            for line in file:
                new_line = line.strip().split('\t')
                if len(new_line) > 0:
                    return_list.append(new_line)
            return return_list

    def print_student_summary(self):
        summary_table = PrettyTable()
        summary_table.field_names = ['cwid', 'name', 'major', 'completed courses', 'remaining required', 'remaining electives']
        for student in self.student_list.values():
            line = student.generate_student_summary()
            line.append(sorted(self.major_list[line[2]]['R'].difference(line[3])))
            if len(self.major_list[line[2]]['E'].difference(line[3])) == len(self.major_list[line[2]]['E']):
                line.append(sorted(self.major_list[line[2]]['E']))
            else:
                line.append('None')
            summary_table.add_row(line)
        print(summary_table)

    def print_instructor_summary(self):
        summary_table = PrettyTable()
        summary_table.field_names = ['cwid', 'name', 'department', 'course', 'student_amount']
        for instructor in self.instructor_list.values():
            for item in instructor.generate_instructor_summary():
                summary_table.add_row(item)
        print(summary_table)

    def print_major_summary(self):
        summary_table = PrettyTable()
        summary_table.field_names = ['dept', 'required', 'electives']
        for dept,flag in self.major_list.items():
            summary_table.add_row([dept, sorted(flag['R']), sorted(flag['E'])])
        print(summary_table)

    @staticmethod
    def sql_test():
        db = sqlite3.connect('/Users/wangshuai/810_startup.db')
        sql = """ select i.CWID, i.Name, i.Dept, g.Course, count(g.Student_CWID)
                  from HW11_instructors as i, HW11_grades as g
                  where i.CWID = g.Instructor_CWID
                  group by i.CWID, g.Course """
        table = PrettyTable()
        table.field_names = ['cwid', 'name', 'department', 'course', 'student_amount']
        for row in db.execute(sql):
            table.add_row(row)
        print(table)



class ProjectTest(unittest.TestCase):
    sit = University()
    sit.get_student_info('/Users/wangshuai/Downloads/students.txt')
    sit.get_instructor_info('/Users/wangshuai/Downloads/instructors.txt')
    sit.get_grade_info('/Users/wangshuai/Downloads/grades.txt')
    sit.get_major_info('/Users/wangshuai/Downloads/majors.txt')
    sit.print_student_summary()
    sit.print_instructor_summary()
    sit.print_major_summary()
    sit.sql_test()

    def test_student(self):
        def test_major(self):
            correct_result = {'SFEN': {'R': {'SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'},
                                 'E': {'CS 501', 'CS 513', 'CS 545'}},
                        'SYEN': {'R': {'SYS 612', 'SYS 671', 'SYS 800'},
                                 'E': {'SSW 540', 'SSW 565', 'SSW 810'}}}
            test_result = dict()
            for major, infomation in self.sit.major_list.items():
                test_result[major] = {flag: courses for flag, courses in infomation.items()}
            self.assertEqual(correct_result, test_result)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
