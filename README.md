# Serendipity
帮助反馈的程序

## 程序描述

这是一个可以自动反馈的程序

## 输入格式

一张图片，表格样例文件在 \Excel 里


## 部署前准备

一台装有Python的服务器，钉钉群（2个）

### 修改config里 [prefeedback] 和 [feedback] 指向钉钉群机器人

```
[prefeedback]
webhook = 
secret = 
[feedback]
webhook = 
secret = 
```

### 修改 Serendipity.py 127行 单引号内的数值，此数值为反馈时间

```
if (Time == '19' and b):
```

### 修改 find_image.py 24行、55行引号内设置部署的网页指向ans.txt    (126行指向files文件夹)

```
if get_task.download_by_url("php/files/ans.txt") == False:
```

### 修改 Serendipity.py 24行，并修改find.py全部，使其与答题卡对应	[e.g.] (以 u + " + 姓名 + " + ", 格式)

```
students = [	#学生名单	按照答题卡横着填写
	u"张三",
	]
```

至此，修改部分完成，当然还有其他部分可以修改

## 部署

### 运行

```
cd Serendipity
Python environment_set.py
```

### Enjoy!


## 提示

网站源码在 \Web 里
程序源码在 \Serendipity 里
示例答题卡在 \Excel 里
主要程序是 Serendipity.py (至于 real_time_object_detection.py 看看就好，没完工，但是可以执行)
