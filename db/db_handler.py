"""
用来保存和获取数据
"""

import os
import pickle
from conf import settings

# 保存数据
def save_data(obj):
    # 1. 获取对象的保存文件的路径
    # 以 类名 当做文件夹的名字
    # obj.__class__ 获取当前对象的类
    # obj.__class__.__name__ 获取当前对象的类的名字
    class_name = obj.__class__.__name__
    user_dir_path = os.path.join(
        settings.DB_PATH, class_name
    )

    # 2. 判断文件夹是否存在，不存在则创建文件夹
    if not os.path.exists(user_dir_path):
        os.mkdir(user_dir_path)

    # 3. 拼接当前用户的pickle文件名字，以用户作为文件名
    user_path = os.path.join(
        user_dir_path,
        obj.user  #当前用户名字
    )

    # 4. 打开文件保存对象，通过 pickle 来处理
    with open(user_path,mode='wb') as f:
        pickle.dump(obj, f)



# 获取数据
def select_data(cls, username):  # 类， username
    class_name = cls.__name__
    user_dir_path = os.path.join(
        settings.DB_PATH, class_name
    )

    user_path = os.path.join(
        user_dir_path,
        username  #当前用户名字
    )
    # 判断文件如果存在，打开，返回， 若不存在，则代表用户不存在
    if os.path.exists(user_path):
        with open(user_path, mode='rb') as f:
            obj = pickle.load(f)
            return obj
    return None