from datetime import datetime
from msilib.schema import Class, Error
import telegram
import os
from .variables import Things

class TelegramSend:

    def __init__(self, dup_01_total, dup_01_occupied, dup_02_total, dup_02_occupied, dup_01_list_str, dup_02_list_str, text):
        self.dup_01_total = dup_01_total
        self.dup_01_occupied = dup_01_occupied
        self.dup_02_total = dup_02_total
        self.dup_02_occupied = dup_02_occupied
        self.dup_01_list_str = dup_01_list_str
        self.dup_02_list_str = dup_02_list_str
        self.text = text
        self.token = Things.telegram_token
        self.chat_id = Things.telegram_chat_id

    def Send(self):
        # result = datetime.today().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f초")
        result = datetime.today().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        tmpstr = f"""⚰️운영 웹서비스에 데이터 전송함
📌전송시간 : {result}
01 전체/사용중 : {self.dup_01_total}/{self.dup_01_occupied}
02 전체/사용중 : {self.dup_02_total}/{self.dup_02_occupied}
         
📌01 리스트
{self.dup_01_list_str}
         
📌02 리스트 
{self.dup_02_list_str}"""

        try:
            bot = telegram.Bot(self.token)
            bot.sendMessage(chat_id=self.chat_id,
                            text=(self.text if self.text else tmpstr)+f'\n💻{os.getlogin()}')
        except Error as e:
            print('telegram send error\n'+e)

    def SendImage(self, hsp_tp_nm, image_path):
        result = datetime.today().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        tmpstr = f'⚰️{hsp_tp_nm} 이미지 \n({result} 기준)\n'
        try:
            bot = telegram.Bot(self.token)
            bot.sendMessage(chat_id=self.chat_id,
                            text=tmpstr+f'\n💻{os.getlogin()}')
            bot.sendPhoto(chat_id=self.chat_id, photo=open(image_path, 'rb'),)
        except Error as e:
            print('telegram send error\n'+e)
