from datetime import datetime
from distutils.log import error
from zeep.transports import Transport
from zeep import Client
import requests
from .variables import Things

# soap 모듈


class PassingDataviaSOAP:
    #soap 방식으로 웹서비스 호출함.
    def SetFuneralData(hsp_tp_cd, occupied, total):
        try:
            with requests.Session() as session:
                transport = Transport(session=session)
            client = Client(
                Things.web_url, transport=transport)
            # result = client.service.Getcurrectors("Python")
            # print(result)
            result = client.service.HomepageFuneralRoomInsert(
                hsp_tp_cd, datetime.today().strftime("%Y-%m-%d"), str(occupied), str(total))
            print(result)
        except error as e:
            print(e)
