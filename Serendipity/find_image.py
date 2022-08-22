from encodings import utf_8
import string
from time import strftime
import requests as req
import datetime
import get_task
import log_write
import sys

Time = 0

def find_txt_line():
	path = str(sys.argv[0])[:-14]
	list = ["", "", ""]
	back_erro = "T"
	global Time

	# # print("保存文件ans.txt")
	""" # 保存文件   from: https://blog.csdn.net/m0_67401920/article/details/125241333
	f = open("/home/rainyangty/Desktop/Chinese_help/ans.txt", "wb+")
	f.write(webtxt.content)
	f.close() """

	if get_task.download_by_url("php/files/ans.txt") == False:
		return False

	# # print("读取文件ans.txt")
	# log_write.log_write("info", "read ans.txt From local/get_task/ans.txt")
	# 读取文件  from: https://dandelioncloud.cn/article/details/1513154346727587842
	try:
		f = open(path + "get_task/ans.txt", "r", encoding="UTF-8")
		file_txt_read = f.readlines()    #读取
	except UnicodeDecodeError:
		# print("ans.txt文件编码错误，尝试GB2312")
		log_write.log_write("Error", "UnicodeDecodeError at local/get_task/ans.txt, try gb2312")
		try:
			f = open(path + "get_task/ans.txt", "r", encoding="gb2312")
			file_txt_read = f.readlines()    #读取
		except UnicodeError:
			return False
	return len(file_txt_read)
	
def find_image():
	path = str(sys.argv[0])[:-14]
	list = ["", "", ""]
	back_erro = "T"
	global Time

	# print("保存文件ans.txt")
	""" # 保存文件   from: https://blog.csdn.net/m0_67401920/article/details/125241333
	f = open("/home/rainyangty/Desktop/Chinese_help/ans.txt", "wb+")
	f.write(webtxt.content)
	f.close() """

	if get_task.download_by_url("php/files/ans.txt") == False:
		# print("下载失败")
		log_write.log_write("warning", "failed to download ans.txt")
		list[2] = "F"
		return list

	# print("读取文件ans.txt")
	log_write.log_write("info", "read ans.txt From local/get_task/ans.txt")
	# 读取文件  from: https://dandelioncloud.cn/article/details/1513154346727587842
	try:
		f = open(path + "get_task/ans.txt", "r", encoding="UTF-8")
		file_txt_read = f.readlines()    #读取
	except UnicodeDecodeError:
		# print("ans.txt文件编码错误，尝试GB2312")
		log_write.log_write("Error", "UnicodeDecodeError at local/get_task/ans.txt, try gb2312")
		try:
			f = open(path + "get_task/ans.txt", "r", encoding="gb2312")
			file_txt_read = f.readlines()    #读取
		except UnicodeError:
			# print("ans.txt文件编码错误")
			log_write.log_write("Error", "UnicodeDecodeError at local/get_task/ans.txt")
			list[2] = "F"
			return list
	last_txt = file_txt_read[len(file_txt_read) - 1]    #读取最后一行
	# last_txt = last_txt.replace('\n','')
	# print("最后一行：" + last_txt)
	log_write.log_write("info", "read ans.txt last line: " + last_txt)

	txt_time = ""
	try:
		for i in range(0, 10, 1):
			txt_time += last_txt[i]
		# print("最后一次上传时间：" + txt_time)
		log_write.log_write("info", "read ans.txt last time that uploaded the image: " + txt_time)
	except IndexError:
		# print("时间数组越界")
		log_write.log_write("Error", "IndexError: out of range of $(last_txt)")
		list[2] = "F"
		return list

	# 获取年月日并进行比对  use datetime from: https://www.jb51.net/article/248438.htm  &&  https://blog.csdn.net/weixin_47912255/article/details/123886297 格式化时间去零
	now = datetime.datetime.now()
	time = now.strftime("%Y/%m/%d")
	# print("现在时间：" + time)
	log_write.log_write("info", "get time now: " + time)

	# 写入任务
	task = ""
	if time == txt_time:
		# print("时间符合\n读取任务")
		log_write.log_write("info", "(txt_time) ==  (time) now")
		i = 11
		while last_txt[i] != "_":
			task += last_txt[i]
			i += 1
	else:
		list[2] = "F"
		return list

	# print("任务：" + task)
	log_write.log_write("info", "read ans.txt task: " + task)

	# print("获取对应涂卡文件名")
	#下载答题卡图片
	file_name = ""
	i += 1
	for a in range(i, len(last_txt) - 1, 1):
		file_name += last_txt[a]
	# print("文件名：" + file_name)
	log_write.log_write("info", "read ans.txt image name: " + file_name)

	if get_task.download_by_url("php/files/" + file_name) == False:
		# print("下载失败")
		list[2] = "F"
		return list
		

	list[0] = task
	list[1] = path + "get_task/" + file_name

	""" if back_erro == "T":
		list[2] = "T"
	else:
		list[2] = "F" """
	
	return list
	# # print(file_name)

# find_image()
