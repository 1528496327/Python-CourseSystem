"""
公共方法
"""


# 多用户登录认证有参装饰器
def auth(role):
    """
    :param role: 角色 ==》 管理员、学生、老师
    :return:
    """
    from core import admin, student, teacher

    def login_auth(func):
        def inner(*args, **kwargs):
            if role == 'admin':
                if admin.admin_info['user']:
                    res = func(*args, **kwargs)
                    return res
                else:
                    print('请先登录管理员账号')
                    admin.login()

            elif role == 'teacher':
                if teacher.teacher_info['user']:
                    res = func(*args, **kwargs)
                    return res
                else:
                    print('请先登录老师账号')
                    teacher.login()

            elif role == 'student':
                if student.student_info['user']:
                    res = func(*args, **kwargs)
                    return res
                else:
                    print('请先登录学生账号')
                    student.login()
            else:
                print('当前视图没有权限！')
        return inner
    return login_auth
