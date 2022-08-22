# from cv2 import initUndistortRectifyMap #文件操作
#import handleC	#自定义头文件
from dingtalkchatbot.chatbot import DingtalkChatbot#以下代码改自 https://github.com/zhuifengshen/DingtalkChatbot
# from 答题卡OpenCV import cv_show
# from CV2 import Cv2	#调用方法源于	https://jingyan.baidu.com/article/e6c8503cb72e7de54f1a182e.html
# import schedule
import time		#定时执行任务	From https://blog.csdn.net/I_m_the_king/article/details/124274340
import datetime
import time
from log_write import log_write
import find_image
import set_config

STU_LIST = {}
UNSTU_LIST = ""	#声明string类变量，用于存储未完成同学
TOTAL = 0

list = set_config

# 初始化机器人
robot = DingtalkChatbot(set_config.getConfig("config", "prefeedback", "webhook"), set_config.getConfig("config", "prefeedback", "secret"))  # 小群预反馈
classrobot = DingtalkChatbot(set_config.getConfig("config", "feedback", "webhook"), set_config.getConfig("config", "feedback", "secret")) # 班级反馈机器人

students = [	#学生名单	按照答题卡横着填写

	]

def add_stu(num):
	global UNSTU_LIST
	UNSTU_LIST += "\n" + students[num]	#将没完成的写入列表

def findunfinished(stu_list):
	global TOTAL
	for i in range(0, len(stu_list), 1):
		if stu_list[i] == "F":
			add_stu(i)
			TOTAL += 1
	

def sendmessage(task, path1):
	global STU_LIST
	global UNSTU_LIST
	UNSTU_LIST = ""
	from find import find
	stu_list = find(path1)
	if stu_list != False:
		findunfinished(stu_list)
	else:
		log_write("warning", "Something wrong in checking students...")
		return False
	
	robot.send_text(msg=u'请检查是否正确，若错误，换一个拍摄角度，重新上传即可', is_at_all=False)
	if(TOTAL == 0):
		robot.send_text(msg=u'今日语文任务：' + task + u'\n全班全部完成 (o゜▽゜)', is_at_all=False)
		# print(u'今日语文任务：\n' + task + u'\n全班全部完成 (o゜▽゜)')
		log_write("info", "\n\n---------------------------------------\n")
		log_write("info", u"Today's task：" + task + u"\nAll of the students in class are finished! (o゜▽゜)")
		log_write("info", "\n\n---------------------------------------\n")
	else:
		robot.send_text(msg=u'今日语文任务：' + task + u'\n未完成名单：' + str(TOTAL) + "/49" + UNSTU_LIST + u'\n缓交时间：明天下午2点前', is_at_all=False)
		# print(u'今日语文任务：\n' + task + u'\n未完成名单：' + UNSTU_LIST + u'\n缓交时间：明天下午2点前')
		log_write("info", "\n\n---------------------------------------\n")
		log_write("info", u"Today's task: " + task + u"\nUnfinish students: " + str(TOTAL) + "/49" + UNSTU_LIST + u"\nHand in time：Before 2 o'clock tomorrow")
		log_write("info", "\n\n---------------------------------------\n")
	
	
	# robot = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
	# Text消息@所有人


a = 0	# 判断是否需要再次检测	0为需要，1为不必
b = False #job()函数是否执行
task = ""

def job():
	if(TOTAL == 0):
		classrobot.send_text(msg=u'今日语文任务：' + task + u'\n全班全部完成 (o゜▽゜)', is_at_all=False)
		# print(u'今日语文任务：\n' + task + u'\n全班全部完成 (o゜▽゜)')
		log_write("info", "\n\n---------------------------------------\n")
		log_write("info", u"Today's task：" + task + u"\nAll of the students in class are finished! (o゜▽゜)")
		log_write("info", "\n\n---------------------------------------\n")
	else:
		classrobot.send_text(msg=u'今日语文任务：' + task + u'\n未完成名单：' + UNSTU_LIST + u'\n缓交时间：明天下午2点前', is_at_all=False)
		# print(u'今日语文任务：\n' + task + u'\n未完成名单：' + UNSTU_LIST + u'\n缓交时间：明天下午2点前')
		log_write("info", "\n\n---------------------------------------\n")
		log_write("info", u"Today's task: " + task + u"\nUnfinish students: " + str(TOTAL) + "/49" + UNSTU_LIST + u"\nHand in time：Before 2 o'clock tomorrow")
		log_write("info", "\n\n---------------------------------------\n")


# job函数预执行，这样当真正需要反馈的时候直接使用此函数算出的结果
def yujob():
	log_write("info", "\n\n***************************************\n")
	global a, task
	list = find_image.find_image()
	if list[2] != "F":
		if sendmessage(list[0], list[1]) == False:
			return False
		else:
			task = list[0]
			return True
	else:
		return False

robot.send_text(msg = u"系统已启动，反馈时间为 19 时")

total_line_last = 1	 #代表之前获取的列数，当列数不一致时开始尝试获取 
while 1 == 1:	#每5分钟获取一次
	now = datetime.datetime.now()
	Time = now.strftime("%H")
	if(b == False):
		total_line = find_image.find_txt_line()
		if (total_line != False and total_line != total_line_last):
			total_line_last = total_line
			if yujob() == False:
				# print("系统检测到今日任务已提交但无法获取，将在 5 分钟后再次检测")
				robot.send_text(msg=u"系统检测到今日任务已提交但无法获取，将在 5 分钟后再次检测", is_at_all=False)
				log_write("warning", "faild to find today's task, it will retry 5 minutes later......")
				time.sleep(300)
			else:
				# print("今日任务获取完毕，即将在 19 时反馈")
				b = True
				robot.send_text(msg=u"今日任务获取完毕，即将在 19 时反馈", is_at_all=False)
				log_write("info", "Finish getting todays task, it will upload at 19 o'clock......")

	if (Time == '19' and b):
		job()
		robot.send_text(msg=u"今日任务反馈完毕	ヽ(✿ﾟ▽ﾟ)ノ", is_at_all=False)
		log_write("info", "Finish, Sleep 23H......")
		b = False
		time.sleep(82800)

	time.sleep(300)
