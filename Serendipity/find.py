from re import T
from time import sleep
import cv2
from Edge_Detection import edge, real_time_edge
import log_write
import fixed_pos

blue: int
green: int
red: int
blue_white: int
red_white: int
green_white: int
x_start_1: int    #声明检测的那些列
x_start_white_1: int
x_start_2: int
x_start_white_2: int

# 获取图片坐标rgb值     From: https://blog.csdn.net/weixin_42259833/article/details/124423177
def get_pix_rgb(img, x: int, y: int, white: bool):
	if(white):
		log_write.log_write("info", "get referenced area (" + str(x) + "," + str(y) + ") RGB")
		global blue_white, green_white, red_white
		""" ext = os.path.basename(image_path).strip().split('.')[-1]
		if ext not in ['png', 'jpg']:
			raise Exception('format error')
		img = cv2.imread(image_path) """
		px = img[y, x]
		# blue_white = img[y, x, 0]
		blue_white = img[y, x]
		# green_white = img[y, x, 1]
		green_white = img[y, x]
		# red_white = img[y, x, 2]
		red_white = img[y, x]
		# log_write.log_write("info", "Finish get RGB: " + red_white + " " + green_white + " " + blue_white)
		log_write.log_write("info", "Finish get RGB")
	else:
		log_write.log_write("info", "get checked area (" + str(x) + "," + str(y) + ") RGB")
		global blue, green, red
		""" ext = os.path.basename(image_path).strip().split('.')[-1]
		if ext not in ['png', 'jpg']:
			raise Exception('format error')
		img = cv2.imread(image_path) """
		px = img[y, x]
		# blue = img[y, x, 0]
		blue = img[y, x]
		# green = img[y, x, 1]
		green = img[y, x]
		# red = img[y, x, 2]
		red = img[y, x]
		""" # print(blue)
		# print("\n")
		# print(green)
		# print("\n")
		# print(red) """
		#return blue, green, red
		log_write.log_write("info", "Finish get RGB (" + str(red) + "," + str(green) + "," + str(blue) + ")")
	

# 获取需要检测的列，避免接下来检测做无用功
def knowlist(start, img, x, y, x_white, y_white):
	day = 5		# 一张可使用天数
	log_write.log_write("info", "Start to get line which needs to be checked")
	global x_start_1, x_start_white_1, x_start_2, x_start_white_2
	if start >= 0:
		# img = cv2.imread(pos)
		# cv2.circle(img, (x[start], y[0]), 5, (0, 0, 255))
		get_pix_rgb(img, x[start], y[0], False)
		get_pix_rgb(img, x_white[start], y_white[0], True)
		red_float = 0.0
		green_float = 0.0
		blue_float = 0.0
		if (red_white != 0):
			red_float = red / red_white
		else:
			red_float = 1.7976931348623157e+308
		if (green_white != 0):
			green_float = green / green_white
		else:
			green_float = 1.7976931348623157e+308
		if (blue_white != 0):
			blue_float = blue / blue_white
		else:
			blue_float = 1.7976931348623157e+308
		if(red_float < 0.1 and green_float < 0.1 and blue_float < 0.1):
			x_start_1 = x[start]
			x_start_white_1 = x_white[start]
			x_start_2 = x[start + day]
			x_start_white_2 = x_white[start + day]
			return
		else:
			knowlist(start - 1, img, x, y, x_white, y_white)
	else:
		x_start_1 = x[0]
		x_start_white_1 = x_white[0]
		x_start_2 = x[day]
		x_start_white_2 = x_white[day]

def find(pos):
	global blue_white, green_white, red_white, x_start_1, x_start_white_1, x_start_2, x_start_white_2

	log_write.log_write("info", "Open image and exchange the size")
	a = edge(pos)   #如果为False则表示获取文件失败
	try:
		if a.any() != False:
			fixed_pos.fixed_pos(a)
			img = cv2.resize(a, (1036, 1473))
			img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

			# 二值化图像	from:https://blog.csdn.net/ljx1400052550/article/details/114735364
			# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   ##要二值化图像，必须先将图像转为灰度图
			ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
			# print("threshold value %s" % ret)  #打印阈值，超过阈值显示为白色，低于该阈值显示为黑色
		else:
			return False
	except:
		return False
	log_write.log_write("info", "Finish opening image and exchanging the size")
	#图像坐标轴左上角为(0, 0),x:横轴,y:纵轴
	x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	x_white = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	y_white = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	a = 0

	# 答题卡颜色部分坐标导入
	withx = 88
	heighty = 55
	for i in range(160, 160 + withx * 5, withx):
		x[a] = i
		x_white[a] = i - 45
		a += 1
	for i in range(160 + withx * 4 + 105, 160 + withx * 9 + 105, withx):
		x[a] = i
		x_white[a] = i - 45
		a += 1
	a = 0
	for i in range(107, 107 + heighty * 25, heighty):
		y[a] = i
		y_white[a] = i - 30
		a += 1

	#get_pix_rgb(pos, 137, 105)
	#get_pix_rgb(pos, x[0], y[0])

	# 确定需要检测的横坐标
	start = knowlist(4, img, x, y, x_white, y_white)
	log_write.log_write("info", "Finish getting line which needs to be checked")


	""" for i in range(0, len(x), 1):
		for j in range(0, len(y), 1):
			cv2.circle(img, (x[i], y[j]), 5, (255, 255, 255))
			cv2.circle(img, (x_white[i], y_white[j]), 5, (0, 255, 0)) """

	STU_ID_TF = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

	cv2.circle(img, (x_start_1, y[0]), 5, (0, 0, 255))
	cv2.circle(img, (x_start_white_1, y_white[0]), 5, (0, 0, 255))
	#标志启用格
	
	# cv2.namedWindow("image", cv2.WINDOW_NORMAL) # 防止显示不全 From: https://blog.csdn.net/qq_42482078/article/details/123319439
	# cv2.imshow("image", img)
	# cv2.waitKey(0)

	# 检测时刻
	log_write.log_write("info", "Checking the students")

	for j in range(1, len(y), 1):   #左边
		get_pix_rgb(img, x_start_1, y[j], False)
		get_pix_rgb(img, x_start_white_1, y_white[j], True)
		red_float = 0.0
		green_float = 0.0
		blue_float = 0.0
		if (red_white != 0):
			red_float = red / red_white
		else:
			red_float = 1.7976931348623157e+308
		if (green_white != 0):
			green_float = green / green_white
		else:
			green_float = 1.7976931348623157e+308
		if (blue_white != 0):
			blue_float = blue / blue_white
		else:
			blue_float = 1.7976931348623157e+308
		if(red_float < 0.4 and green_float < 0.4 and blue_float < 0.4):
			cv2.circle(img, (x_start_1, y[j]), 5, (255, 255, 255))
			STU_ID_TF[j - 1] = "T"
			log_write.log_write("info", "STU[" + str(j) + " T" + "]: " + str(red_float) + "," + str(green_float) + "," + str(blue_float))
		else:
			STU_ID_TF[j - 1] = "F"
			log_write.log_write("warning", "STU[" + str(j) + " F" + "]: " + str(red_float) + "," + str(green_float) + "," + str(blue_float))
		cv2.circle(img, (x_start_white_1, y_white[j]), 5, (0, 255, 0))

	for j in range(0, len(y), 1):   #右边
		get_pix_rgb(img, x_start_2, y[j], False)
		get_pix_rgb(img, x_start_white_2, y_white[j], True)
		red_float = 0.0
		green_float = 0.0
		blue_float = 0.0
		if (red_white != 0):
			red_float = red / red_white
		else:
			red_float = 1.7976931348623157e+308
		if (green_white != 0):
			green_float = green / green_white
		else:
			green_float = 1.7976931348623157e+308
		if (blue_white != 0):
			blue_float = blue / blue_white
		else:
			blue_float = 1.7976931348623157e+308
		if(red_float < 0.4 and green_float < 0.4 and blue_float < 0.4):
			cv2.circle(img, (x_start_2, y[j]), 5, (255, 255, 255))
			STU_ID_TF[j + 24] = "T"
			log_write.log_write("info", "STU[" + str(j + 25) + " T" + "]: " + str(red_float) + "," + str(green_float) + "," + str(blue_float))
		else:
			STU_ID_TF[j + 24] = "F"
			log_write.log_write("warning", "STU[" + str(j + 25) + " F" + "]: " + str(red_float) + "," + str(green_float) + "," + str(blue_float))
		cv2.circle(img, (x_start_white_2, y_white[j]), 5, (0, 255, 0))
		
	# cv2.imshow("image", img)
	# cv2.waitKey(0)
	return STU_ID_TF

def real_time_find(imgage):
	global blue_white, green_white, red_white, x_start_1, x_start_white_1, x_start_2, x_start_white_2

	# 直接指定目标帧大小
	a = real_time_edge(imgage)
	if (type(a) != bool):
		img = fixed_pos.fixed_pos(a)
		img = cv2.resize(a, (1036, 1473))
		ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		# img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		#图像坐标轴左上角为(0, 0),x:横轴,y:纵轴
		x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		x_white = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		y_white = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		a = 0

		# 答题卡颜色部分坐标导入
		withx = 88
		heighty = 55
		for i in range(160, 160 + withx * 5, withx):
			x[a] = i
			x_white[a] = i - 45
			a += 1
		for i in range(160 + withx * 4 + 105, 160 + withx * 9 + 105, withx):
			x[a] = i
			x_white[a] = i - 45
			a += 1
		a = 0
		for i in range(107, 107 + heighty * 25, heighty):
			y[a] = i
			y_white[a] = i - 30
			a += 1

		#get_pix_rgb(pos, 137, 105)
		#get_pix_rgb(pos, x[0], y[0])

		# 确定需要检测的横坐标
		start = knowlist(5, img, x, y, x_white, y_white)


		""" for i in range(0, len(x), 1):
			for j in range(0, len(y), 1):
				cv2.circle(img, (x[i], y[j]), 5, (0, 0, 255))
				cv2.circle(img, (x_white[i], y_white[j]), 5, (0, 255, 0)) """

		STU_ID_TF = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

		cv2.circle(img, (x_start_1, y[0]), 5, (255, 255, 255))
		cv2.circle(img, (x_start_white_1, y_white[0]), 5, (0, 0, 255))
		#标志启用格
		
		# cv2.namedWindow("image", cv2.WINDOW_NORMAL) # 防止显示不全 From: https://blog.csdn.net/qq_42482078/article/details/123319439
		# cv2.imshow("image", img)
		# cv2.waitKey(0)

		# 检测时刻

		for j in range(1, len(y), 1):   #左边
			get_pix_rgb(img, x_start_1, y[j], False)
			get_pix_rgb(img, x_start_white_1, y_white[j], True)
			red_float = 0.0
			green_float = 0.0
			blue_float = 0.0
			if (red_white != 0):
				red_float = red / red_white
			else:
				red_float = 1.7976931348623157e+308
			if (green_white != 0):
				green_float = green / green_white
			else:
				green_float = 1.7976931348623157e+308
			if (blue_white != 0):
				blue_float = blue / blue_white
			else:
				blue_float = 1.7976931348623157e+308
			if(red_float < 0.4 and green_float < 0.4 and blue_float < 0.4):
				cv2.circle(img, (x_start_1, y[j]), 5, (255, 255, 255))
				STU_ID_TF[j - 1] = "T"
			else:
				STU_ID_TF[j - 1] = "F"
			cv2.circle(img, (x_start_white_1, y_white[j]), 5, (0, 255, 0))

		for j in range(0, len(y), 1):   #右边
			get_pix_rgb(img, x_start_2, y[j], False)
			get_pix_rgb(img, x_start_white_2, y_white[j], True)
			red_float = 0.0
			green_float = 0.0
			blue_float = 0.0
			if (red_white != 0):
				red_float = red / red_white
			else:
				red_float = 0.0
			if (green_white != 0):
				green_float = green / green_white
			else:
				green_float = 0.0
			if (blue_white != 0):
				blue_float = blue / blue_white
			else:
				blue_float = 0.0
			if(red_float < 0.2 and green_float < 0.2 and blue_float < 0.2):
				cv2.circle(img, (x_start_2, y[j]), 5, (255, 255, 255))
				STU_ID_TF[j + 24] = "T"
			else:
				STU_ID_TF[j + 24] = "F"
			cv2.circle(img, (x_start_white_2, y_white[j]), 5, (0, 255, 0))
			
		cv2.imshow("image", img)
		# print(STU_ID_TF)
		# sleep(1)
		cv2.waitKey(0)