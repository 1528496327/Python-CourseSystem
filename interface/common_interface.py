"""
公共接口
"""
import os
from conf import settings
from db import models


# 获取所有学校名称接口
def get_all_school_interface():
    # 1.获取学校文件夹路径
    school_dir = os.path.join(
        settings.DB_PATH, 'School'
    )

    # 2.判断文件夹是否存在
    if not os.path.exists(school_dir):
        return False, '没有学校，请先联系管理员'

    # 3.文件夹若存在，获取文件夹中所有文件的名字
    school_list = os.listdir(school_dir)
    return True, school_list


# 公共登录接口
def login_interface(user, pwd, user_type):
    if user_type == 'admin':
        obj = models.Admin.select(user)

    elif user_type == 'student':
        obj = models.Student.select(user)

    elif user_type == 'teacher':
        obj = models.Teacher.select(user)
    else:
        return False, '登录角色不对，请输入角色'

    # 1. 判断用户是否存在
    # 2. 若用户存在，则校验密码
    if obj:
        if pwd == obj.pwd:
            return True, '登录成功！'
        else:
            return False, '密码错误！'
    else:
        # 3. 若不存在，则证明用户不存在并返回视图层
        return False, '用户名不存在'


# 获取学校下所有课程接口
def get_course_in_school_interface(school_name):
    # 1.获取学校对象
    school_obj = models.School.select(school_name)

    # 2.获取学校对象下所有课程
    course_list = school_obj.course_list

    if not course_list:
        return False, '该学校没有课程'
    else:
        return True, course_list
