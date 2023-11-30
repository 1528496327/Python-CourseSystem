"""
老师接口层
"""
from db import models

# 老师查看课程接口
def check_course_interface(teacher_name):
    # 1.获取当前老师对象
    teacher_obj = models.Teacher.select(teacher_name)

    # 2.判断老师对象中课程列表是否有值
    course_list = teacher_obj.course_list_from_teacher

    # 3.若有则返回True，无则返回False
    if not course_list:
        return False, '老师没有选择课程'
    return True, course_list

# 老师添加课程接口
def add_course_interface(course_name, teacher_name):
    # 1.获取当前老师对象
    teacher_obj = models.Teacher.select(teacher_name)

    # 2.判断当前课程是否在老师的课程列表中
    # course_list = teacher_obj.course_list_from_teacher
    # 让老师对象，调用查看教授课程方法，返回课程
    course_list = teacher_obj.show_course()
    if course_name in course_list:
        return False, '该课程已存在！'

    # 3.如果不存在，则添加该课程到老师的课程列表
    teacher_obj.add_course(course_name)
    return True, f'添加课程 [{course_name}] 成功'


# 老师获取课程下学生接口
def get_student_interface(course_name, teacher_name):
    # 1.获取当前老师对象
    teacher_obj = models.Teacher.select(teacher_name)

    # 2.让当前老师对象，调用获取课程下所有学生功能
    student_list = teacher_obj.get_student(course_name)

    # 3.判断课程下是否有学生
    if not student_list:
        return False, '学生没有选择该课程'
    return True, student_list

# 老师修改分数接口
def change_score_interface(course_name, student_name, score, teacher_name):
    # 1.获取老师对象
    teacher_obj = models.Teacher.select(teacher_name)

    # 2.让老师对象调用修改分数方法
    teacher_obj.change_score(course_name, student_name, score)
    return True, '修改分数成功！'