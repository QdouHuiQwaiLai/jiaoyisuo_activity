import requests
import os
import sys
import logging
import hmac, base64, struct, hashlib, time

import random
requests.packages.urllib3.disable_warnings()

o_path = os.getcwd()  # 返回当前工作目录
sys.path.append('../')

logger = logging.getLogger(__name__)  # 定义Logger的名字，之前直接用logging调用的名字是root，日志格式用%(name)s可以获得。这里的名字也可以自定义比如"TEST"
ch = logging.StreamHandler()  # 输出到屏幕的handler
# ch.setLevel(logging.INFO)  # 输出级别和上面的忽略级别都不一样，可以看一下效果
fh = logging.FileHandler('access.log', encoding='utf-8')  # 输出到文件的handler，定义一下字符编码
fh.setLevel(logging.WARNING)
ch_formatter = logging.Formatter('%(name)s %(asctime)s {%(levelname)s}:%(message)s',
                                 datefmt='%Y-%m-%d %H:%M:%S')  # 关键参数datefmt自定义日期格式
fh_formatter = logging.Formatter('%(asctime)s %(module)s-%(lineno)d [%(levelname)s]:%(message)s',
                                 datefmt='%Y/%m/%d %H:%M:%S')
ch.setFormatter(ch_formatter)
fh.setFormatter(fh_formatter)
logger.addHandler(ch)
logger.addHandler(fh)


# 解析文本
def parseUserList(path):
  userList = []
  for line in open(f'./input/{path}'):
    user = str(line.strip('\n')).split("----", )
    userList.append(user)
  return userList


def myLog(count, msg):
  if count != 4:
    logger.error(msg)
  else:
    logger.warning(f'{msg}---------------失败')


# def sendRequests(method, url, usrname, flag, headers, **kwargs):
#   # print(kwargs)
#   jsonValuve = {}
#   cook= {}
#   for i in range(5):
#     try:
#       p = random.choice(allProxy)
#       headers = p['addheaders'](headers, p['authList'], True)
#       response = requests.request(method, url,
#                                   headers=headers,
#                                   proxies=p['proxy'],
#                                   verify=False,
#                                   allow_redirects=False,
#                                   timeout=8.5,
#                                   **kwargs)
#       # print(response.text)
#       jsonValuve = response.json()
#       # print(jsonValuve)
#       cook = response.cookies
#       # if 'errno' not in jsonValuve.keys():
#       #   myLog(i, f'{usrname}-{flag}动作 出错{i + 1}次')
#       #   continue
#     except Exception as e:
#       # print(e)
#       myLog(i, f'{usrname}-{flag}动作 出错{i + 1}次')
#       pass
#     else:
#       if response.status_code == 200:
#         break
#     time.sleep(0.5)
#   return jsonValuve, cook