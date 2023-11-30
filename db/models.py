"""
用来存放类
学校、学员、课程、讲师、管理员类
"""
from db import db_handler


# 父类
class Base:
    # 查看数据  --> 登录、查看数据
    @classmethod
    def select(cls, username):  # 接收到 Admin  和 username
        # obj 有可能是一个对象，也有可能 是 None
        obj = db_handler.select_data(cls, username)
        return obj

    # 保存数据  --> 注册、更新数据用
    def save(self):
        # 让 db_handler 中的 save_data 来保存数据
        db_handler.save_data(self)


# 管理员类
class Admin(Base):
    # 调用类的时候触发
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd

    # 创建学校
    def create_school(self, school_name, school_addr):
        """该方法内部来调用学校类实例化得到的对象，并保存"""
        school_obj = School(school_name, school_addr)
        school_obj.save()

    # 创建课程
    def create_course(self, school_obj, course_name):
        # 1.调用课程类，实例化创建课程
        course_obj = Coures(course_name)
        course_obj.save()
        # 2.获取当前学校对象，并将课程添加到学校对象的课程列表中
        school_obj.course_list.append(course_name)
        # 3.更新学校数据
        school_obj.save()

    # 创建讲师
    def create_teacher(self, teacher_name, teacher_pwd):
        # 1.调用老师类，实例化的老师对象，并保存
        teacher_obj = Teacher(teacher_name, teacher_pwd)
        teacher_obj.save()


# 学校类
class School(Base):
    def __init__(self, name, addr):
        self.user = name
        self.addr = addr
        # 课程列表：每所学校都应该有相应的课程
        self.course_list = []


# 学生类
class Student(Base):
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        # 每个学生只能有一个校区
        self.school = None
        # 一个学生可以选择多门课程
        self.course_list = []
        self.score = {}  # {"course_name": 90}

    # 学生添加学校方法
    def add_school(self, school_name):
        self.school = school_name
        self.save()

    # 学生添加课程方法
    def add_course(self, course_name):
        # 1.学生课程列表绑定课程
        self.course_list.append(course_name)
        # 1.2 给学生选择的课程设置默认分数
        self.score[course_name] = 0
        self.save()
        # 2.学生选择的课程对象绑定学生
        course_obj = Coures.select(course_name)
        course_obj.student_list.append(self.user)
        course_obj.save()


# 课程类
class Coures(Base):
    def __init__(self, course_name):
        self.user = course_name
        self.student_list = []


# 老师类
class Teacher(Base):
    def __init__(self, teacher_name, teacher_pwd):
        # self.user 需要统一
        self.user = teacher_name
        self.pwd = teacher_pwd
        self.course_list_from_teacher = []

    # 老师查看课程方法
    def show_course(self):
        return self.course_list_from_teacher

    # 老师添加课程方法
    def add_course(self, course_name):
        self.course_list_from_teacher.append(
            course_name
        )
        self.save()

    # 老师获取课程下学生方法
    def get_student(self, course_name):
        course_obj = Coures.select(course_name)
        return course_obj.student_list

    # 老师修改学生分数方法
    def change_score(self, course_name, student_name, score):
        # 1.获取学生对象
        student_obj = Student.select(student_name)

        # 2.再给学生对象中的课程修改分数
        student_obj.score[course_name] = score
        student_obj.save()