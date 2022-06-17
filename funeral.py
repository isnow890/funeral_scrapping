from distutils.log import error
import schedule
from datetime import datetime
from zeep.transports import Transport
from zeep import Client
from multiprocessing.sharedctypes import Value
from time import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests, time, re
from selenium.webdriver.common.by import By
import copy
from implements.soapweb import PassingDataviaSOAP
from implements.telegramsend import TelegramSend
from implements.do_it import Doit
import os
import sys

cnt=0
d = Doit() 
te= TelegramSend('','', '','', '', '', '⚰️funeral 프로그램 실행됨.')


def increase_count():
    global cnt
    cnt +=1
    print(f'실행된지 : {str(cnt)}분',flush=True)
    

print ('start')
# os.system('pause')

print ('프로그램 실행함')
print ('실행한지 : 0분')


te.Send()
arg_count = len(sys.argv)

if (arg_count>1):
    if (sys.argv[1] == '-i'):
        te= TelegramSend('','', '','', '', '', '⚰️funeral 프로그램 즉시 옵션으로 실행됨.')
        te.Send()        
        print ('즉시 실행함.')
        d.SetJob()
    else:
        print('잘못된 실행방식입니다. argument는 -i 밖에 없습니다(프로그램 실행 즉시 데이터 전송)\n프로그램을 종료합니다.')
        exit()


#https://pypi.org/project/schedule/

#경과 시간 표시
schedule.every(1).minutes.do(increase_count)
#23시와 23시 05분에 작업 실행.
schedule.every().day.at("23:00").do(d.SetJob)
schedule.every().day.at("23:05").do(d.SetJob)


while True:
    schedule.run_pending()
    time.sleep(1)    