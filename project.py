from prettytable import PrettyTable
from collections import defaultdict


class Student:
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course_map = dict()

    def add_grade(self, course_name, grade):
        self.course_map[course_name] = grade

    def generate_student_summary(self):
        sorted_list = sorted(list(self.course_map.keys()))
        return_list = [self.cwid, self.name, sorted_list]
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
        summary_table.field_names = ['cwid', 'name', 'course']
        for student in self.student_list.values():
            summary_table.add_row(student.generate_student_summary())
        print(summary_table)

    def print_instructor_summary(self):
        summary_table = PrettyTable()
        summary_table.field_names = ['cwid', 'name', 'department', 'course', 'student_amount']
        for instructor in self.instructor_list.values():
            for item in instructor.generate_instructor_summary():
                summary_table.add_row(item)
        print(summary_table)


def main():
    sit = University()
    sit.get_student_info('/Users/wangshuai/Downloads/students.txt')
    sit.get_instructor_info('/Users/wangshuai/Downloads/instructors.txt')
    sit.get_grade_info('/Users/wangshuai/Downloads/grades.txt')
    sit.print_student_summary()
    sit.print_instructor_summary()


if __name__ == '__main__':
    main()
