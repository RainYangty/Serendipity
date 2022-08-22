import sys
import os
path = str(sys.argv[0])
# print("当前目录: " + path[:-18])
ans = "sudo pip install -r " + path[:-18] + "requirements.txt"
os.system(ans)