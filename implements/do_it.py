from distutils.log import error
from mimetypes import init
import schedule
from datetime import datetime
from zeep.transports import Transport
from zeep import Client
from multiprocessing.sharedctypes import Value
from time import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import re
from selenium.webdriver.common.by import By
from .chromedriver_auto_update import ChromeDriverAutoUpdate
from .variables import Things
from implements.soapweb import PassingDataviaSOAP
from implements.telegramsend import TelegramSend


def GetOccupiedCount(x):
    return len({key: value for (key, value) in x.items() if value != '이용가능'})


def RemoveNullProperty(col):
    col_dup = col.copy()

    for key, value in col.items():
        value_trim = value.replace(' ', '')
        key_trim = key.replace(' ', '')
        if (value_trim == '' or key_trim == ''):
            del col_dup[key]
    return col_dup


class Doit:

    def SetJob(self):

        print(f'실행시간 {datetime.today().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")}')
        auto = ChromeDriverAutoUpdate()
        driver_path = auto.DoDownload()

        dic_01 = {}
        dic_02 = {}
        dic_02_2 = {}
        dic_01_dup = {}
        dic_02_dup = {}
        dic_02_2_dup = {}
        tmp_str_01 = ''
        tmp_str_02 = ''

        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=3000x3000')
            options.add_argument("disable-gpu")

            driver = webdriver.Chrome(driver_path, chrome_options=options)
            driver.get(Things.scr_url01)

            html = driver.page_source
            soup = BeautifulSoup(html)

            d_place = soup.select('.map-txt > div')
            d_people = soup.select('.map-name > div')

            print('01 조회함')
            for a in range(0, len(d_place)):
                if a == 0:
                    continue
                # print(f'호실 : {d_place[a].get_text()} 사람 : {d_people[a].get_text()}')
                dic_01[d_place[a].get_text()] = d_people[a].get_text()
                tmp_str_01 += f'\n {d_place[a].get_text()} - {d_people[a].get_text()}'

            element = driver.find_element_by_xpath(
                "//*[@id='content']/div/div[4]/div")
            element.screenshot("shot01.png")

            driver.get(Things.scr_url02)

            html2 = driver.page_source
            soup2 = BeautifulSoup(html2)

            d_place_02 = soup2.select('.map-txt > div')
            d_people_02 = soup2.select('.map-name > div')

            print('02 첫번째 페이지 조회함')
            for a in range(0, len(d_place_02)):
                # print(f'호실 : {d_place_02[a].get_text()} 사람 : {d_people_02[a].get_text()}')
                dic_02[d_place_02[a].get_text()] = d_people_02[a].get_text()
                tmp_str_02 += f'\n{d_place_02[a].get_text()} - {d_people_02[a].get_text()}'

            element = driver.find_element_by_xpath("//*[@id='view1']")
            element.screenshot("shot02-1.png")

            driver.find_element(by=By.XPATH, value='//*[@id="tab2"]/a').click()
            time.sleep(3)

            html2 = driver.page_source

            soup2 = BeautifulSoup(html2)

            d_place_02 = soup2.select('.map-txt > div')
            d_people_02 = soup2.select('.map-name > div')

            print('02 다음 버튼 클릭 후 두번째 페이지 조회함.')
            for a in range(0, len(d_place_02)):
                # print(f'호실 : {d_place_02[a].get_text()} 사람 : {d_people_02[a].get_text()}')
                dic_02_2[d_place_02[a].get_text()] = d_people_02[a].get_text()
                tmp_str_02 += f'\n호실 {d_place_02[a].get_text()} 사람  {d_people_02[a].get_text()}'

            element = driver.find_element_by_xpath("//*[@id='view1']")
            element.screenshot("shot02-2.png")

            dic_01_dup = dic_01.copy()
            dic_02_dup = dic_02.copy()
            dic_02_2_dup = dic_02_2.copy()
            dic_01_dup = RemoveNullProperty(dic_01)
            dic_02_dup = RemoveNullProperty(dic_02)
            dic_02_2_dup = RemoveNullProperty(dic_02_2)
            dic_01_total_cnt = len(dic_01_dup)
            dic_02_total_cnt = len(dic_02_dup)+len(dic_02_2_dup)
            dic_01_occupied = GetOccupiedCount(dic_01_dup)
            dic_02_occupied = GetOccupiedCount(
                dic_02_dup) + GetOccupiedCount(dic_02_2_dup)

            print('dic_01_total_cnt : '+str(dic_01_total_cnt))
            print('dic_02_total_cnt : '+str(dic_02_total_cnt))
            print('dic_01_occupied : '+str(dic_01_occupied))
            print('dic_02_occupied : '+str(dic_02_occupied))

            PassingDataviaSOAP.SetFuneralData(
                '01', dic_01_occupied, dic_01_total_cnt)
            PassingDataviaSOAP.SetFuneralData(
                '02', dic_02_occupied, dic_02_total_cnt)

            # self,dup_01_total,dup_01_occupied, dup_02_total,dup_02_occupied, dup_01_list_str, dup_02_list_str, text

            te = TelegramSend(dic_01_total_cnt, dic_01_occupied,
                              dic_02_total_cnt, dic_02_occupied, tmp_str_01, tmp_str_02, '')
            te.Send()

            #이미지 전송
            te.SendImage("01", "shot01.png")
            time.sleep(1)
            te.SendImage("02-1", "shot02-1.png")
            time.sleep(1)
            te.SendImage("02-2", "shot02-2.png")

        except error as e:
            tmp_error_msg = '에러발생 에러발생 :\n\n'+e
            print(tmp_error_msg)
            te = TelegramSend('', '', '', '', '', '', tmp_error_msg)
            te.Send()
        finally:
            driver.quit()
