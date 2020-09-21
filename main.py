import requests
import sys
import os
import json
from multiprocessing import Process
import time
import random
from hashlib import md5
from multiprocessing import Process
from multiprocessing.dummy import Pool as pool
from multiprocessing import Process
from functools import  partial
import threading
import logging
from threading import Thread
from util.trans_time import utc_to_timestamp, timestamp_to_time_string
from util.hoop import myLog

requests.packages.urllib3.disable_warnings()


def sendRequests(method, url, **kwargs):
  for i in range(5):
    try:
      response = requests.request(method, url,
                                  verify=False,
                                  allow_redirects=False,
                                  timeout=8.5,
                                  **kwargs)
      # print(response.text)
      if response.status_code == 200:
        return response.json()
    except Exception as e:
      # myLog(i, f'{url}动作 出错{i + 1}次')
      print(i, f'{url}动作 出错{i + 1}次')
    time.sleep(0.5)
  return None


class Send():
  @staticmethod
  def send_all(exchange_name, title, time_string, url):
    '''
    发送所有渠道的消息
    :param exchange_name: 交易所名称
    :param title:  公告标题
    :param time_string:  发布时间
    :param url: 连接
    :return: 
    '''
    Send.send_wei(exchange_name, title, time_string, url)   # 发送微信推送
  
  @staticmethod
  def send_wei(exchange_name, title, time_string, url):
    wei_api_list = [
      'SCU104400Tb930e5624897ac99048f19028d063f3c5f0181f667342',
      'SCU105619T1dfc4eb1f60bcbd4c837dcaf938037495f0d245d2e570',
    ]
    for wei_api in wei_api_list:
      send_wei_res = sendRequests('GET', f'https://sc.ftqq.com/'
                                     f'{wei_api}'
                                     f'.send?'
                                     f'text={exchange_name}----{title}&'
                                     f'desp={title}----{time_string}----{url}')
      print(send_wei_res)
  

class DoWatch():
  def __init__(self, exchange_name, main_link, start_time):
    '''
    @:param string exchange_name 交易所名称
    @:param string main_link 主体连接
    @:param string start_time 开始监控的时间
    '''
    self.exchange_name = exchange_name
    self.main_link = main_link
    self.link = f'{main_link}/hc/api/internal/recent_activities?locale=zh-cn&page=1'
    self.start_time = start_time
    self.do_while_watch()  # 开启监控
    
  def do_while_watch(self):
    while True:
      try:
        myLog(0, f'{self.exchange_name}----开始')
        print(f'{self.exchange_name}----开始')
        self.watch()
        time.sleep(5)
      except Exception as e:
        print(f'{self.exchange_name}----错误')
        continue
  
  def watch(self):
    # print(self.link)
    watch_res = sendRequests('GET', self.link, )
    # print(waf'{self.exchange_name}----
    activity_list = sorted(watch_res['activities'], key=lambda activity: utc_to_timestamp(activity['timestamp']))
    for i, activity in enumerate(activity_list):
      current_timestamp = utc_to_timestamp(activity['timestamp'])
      if current_timestamp > self.start_time:
        print(f'{self.exchange_name}----{activity["title"]}----{timestamp_to_time_string(current_timestamp)}----{self.main_link}{activity["url"]}')
        Send.send_all(
          self.exchange_name,
          activity['title'],
          timestamp_to_time_string(current_timestamp),
          f'{self.main_link}{activity["url"]}',
        )
        if i + 1 >= len(activity_list):
          self.start_time = current_timestamp
          print(f'{self.exchange_name}----修改了时间')
    print(self.start_time)


def Go():
  pList = []
  pList.append(Thread(target=DoWatch, args=('ok币', 'https://www.okex.com/support/', 1600581355 )))
  pList.append(Thread(target=DoWatch, args=('火币', 'https://huobiglobal.zendesk.com', 1600684247)))
  for p in pList:
    p.start()
  for p in pList:
    p.join()
    

if __name__ == '__main__':
  # DoWatch('ok币', 'https://okhelp.okex.com', 1600480987)
  # DoWatch('火币', 'https://huobiglobal.zendesk.com', 1600581358)
  # DoWatch('币安', 'https://binance.zendesk.com', 1)
  Go()
  pass


 #  nohup python3 main.py &