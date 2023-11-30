"""
管理员接口
"""
from db import models

# 管理员注册接口
def admin_register_interface(username, password):
    # 1. 判断用户是否存在
    # 调用 Admin 类中的 select_data 方法
    admin_obj = models.Admin.select(username)

    # 1.1 若存在，不允许注册，返回用户已存在给视图层
    if admin_obj:
        return False, '用户已存在！'
    # 1.2 若不存在，允许注册，调用类实例化得到对象并保存到本地
    admin_obj = models.Admin(username, password)
    # 对象调用save() 会将 admin_obj 传给 save() 方法
    admin_obj.save()
    return True, '注册成功'


# 管理员创建学校接口
def create_school_interface(school_name, school_addr, admin_name):
    # 1.查看当前学校是否已存在
    school_obj = models.School.select(school_name)
    # 2.若学校存在，返回False，告诉用户学校已存在
    if school_obj:
        return False, '该学校已存在！'
    # 3.若不存在，则创建学校，注意：由管理员对象创建
    admin_obj = models.Admin.select(admin_name)
    # 由管理员来调用创建学校方法，并传入学校的名字和地址
    admin_obj.create_school(
        school_name, school_addr
    )
    # 4.返回创建学校成功给视图层
    return True, f'{school_name} 创建成功！'


# 管理员创建课程接口
def create_course_interface(school_name, course_name, admin_name):
    # 1.查看课程是否存在
    # 1.1 先获取学校对象中的课程列表
    school_obj = models.School.select(school_name)
    # 1.2 判断当前课程是否存在课程列表中
    if course_name in school_obj.course_list:
        return False, '当前课程已存在！'

    # 1.3 若不存在，由管理员创建课程
    admin_obj = models.Admin.select(admin_name)
    admin_obj.create_course(
        school_obj, course_name
    )

    return True, f'[{course_name}] 课程创建成功，绑定给 [{school_name}]'


# 管理员创建老师接口
def create_teacher_interface(teacher_name, admin_name, teacher_pwd='123'):
    # 1.判断老师是否存在
    teacher_obj = models.Teacher.select(teacher_name)

    # 2.若存在，则返回不能创建
    if teacher_obj:
        return False, '老师已存在，无法重复创建'

    # 3.若不存在，则让管理员创建老师
    admin_obj = models.Admin.select(admin_name)
    admin_obj.create_teacher(teacher_name, teacher_pwd)

    return True, f'[{teacher_name}] 老师创建成功！ '

