import datetime
import time


def utc_to_timestamp(utc_string):
  """
  utc时间转换为当前时间的时间戳
  :param string utc_string utc时间的时间字符串
  :return int 时间戳
  """
  now_time_string = datetime.datetime.strptime(utc_string, "%Y-%m-%dT%H:%M:%SZ")
  localtime = now_time_string + datetime.timedelta(hours=8)
  timestamp = int(localtime.timestamp())
  # print(f'{utc_string}----{localtime}----{timestamp}')
  return timestamp


def timestamp_to_time_string(timestamp):
  '''
  时间戳转换为时间字符串
  :param timestamp: int 时间戳
  :return: string 时间字符串
  '''
  return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))