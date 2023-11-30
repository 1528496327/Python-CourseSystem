"""
学生接口
"""
from db import models


# 学生注册接口
def student_register_interface(username, password):
    # 1. 判断用户是否存在
    # 调用 Student 类中的 select_data 方法
    student_obj = models.Student.select(username)

    # 1.1 若存在，不允许注册，返回用户已存在给视图层
    if student_obj:
        return False, '该学生用户已存在！'
    # 1.2 若不存在，允许注册，调用类实例化得到对象并保存到本地
    student_obj = models.Student(username, password)
    # 对象调用save() 会将 admin_obj 传给 save() 方法
    student_obj.save()
    return True, '注册成功'


# 学生选择学校接口
def add_school_interface(school_name, student_name):
    # 1.先判断当前学生是否存在学校
    student_obj = models.Student.select(student_name)

    if student_obj.school:
        return False, f'当前学生已经存在对应学校 [{student_obj.school}] ，无法重复选择！'

    # 2.若不存在学校，则给调用学生对象中选择学校的方法，实现学生添加学校
    student_obj.add_school(school_name)

    return True, f'选择学校 [{school_name}] 成功！'


# 获取学生所在学校所有课程接口
def get_course_list_interface(student_name):
    # 1.获取当前学生对象
    student_obj = models.Student.select(student_name)
    school_name = student_obj.school
    # 2.判断当前学生有没有学校
    if not student_obj.school:
        return False, '没有学校，请先选择学校！'
    # 3.开始获取学校对象中的课程列表
    school_obj = models.School.select(school_name)
    # 3.1 判断当前学校是否有课程，若没有，联系管理员
    course_list = school_obj.course_list
    if not school_obj.course_list:
        return False, '没有课程，请先联系管理员创建'
    # 3,2 若有则返回课程列表
    return True, course_list


# 学生选择课程接口
def add_course_interface(course_name, student_name):
    # 1.先判断当前学生是否已选择课程
    student_obj = models.Student.select(student_name)

    if course_name in student_obj.course_list:
        return False, f'当前学生已经选择过课程 [{course_name}] ，无法重复选择！'

    # 2.当前学生未选择该课程，则给调用学生对象中选择学校的方法，实现学生添加学校
    student_obj.add_course(course_name)
    return True, f'选择课程 [{course_name}] 成功！'


# 学生查看分数接口
def check_score_interface(student_name):
    student_obj = models.Student.select(student_name)
    score_dict = student_obj.score
    return score_dict
