# From: https://blog.csdn.net/myinsert/article/details/123401069

# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
from encodings import utf_8
import os
import urllib.request
from pathlib import Path
import sys
from log_write import log_write


# 根据图片的资源路径下载图片到本地
def download_by_url(url):
    # 获取当前文件名作为保存文件夹
    path = str(sys.argv[0])[:-14] + "get_task"# os.path.basename(__file__).split('.')[0]
    # 获取 url 中文件名称和扩展名作为保存文件名
    name = url.split('/')[-1]
    # 获取文件扩展名作为文件保存分类
    file_type = name.split('.')[1]
    path += '/'# + file_type
    # 判断文件保存路径是否存在，不存在则创建
    dirs = Path(path)
    if not dirs.is_dir():
        os.makedirs(path)

    # 根据文件路径获取文件，如果文件不存在则创建
    # wb: 以二进制格式打开一个文件只用于写入
    file_path = path + name
    file = open(file_path, 'wb')
    try:
        # 通过 url 获取资源
        request = urllib.request.urlopen(url)
        # 将图片二进制数据写入文件
        file.write(request.read())
        # print('文件保存成功！')
        log_write("info", "Finish downloading the file in " + file_path)
        return True
    except IOError:
        # print('获取文件失败！')
        log_write("warning", "IOError_Can't download the file!")
        return False
    # 关闭文件
    file.close()


# 按间距中的绿色按钮以运行脚本。
""" if __name__ == '__main__':
    download_by_url("https://u1.res.netease.com/pc/gw/20201014103243/img/p3/bg3_33_52a4a14.jpg") """

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助


