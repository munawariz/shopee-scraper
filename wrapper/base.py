import http.client
import json

class BaseWrapper:
    base_url = 'https://shopee.co.id'
    image_base_url = 'https://cf.shopee.co.id/file'
    video_base_url = 'http://play-ws.vod.shopee'

    def __init__(self):
        self.establish_connection()
        self.generate_headers()

    def establish_connection(self):
        self.connection = http.client.HTTPSConnection('shopee.co.id')

        return self.connection

    def generate_headers(self):
        self.headers = {
            'Cookie': 'REC_T_ID=6bab0c7a-f8f1-11ec-a247-2cea7f4774b9; SPC_F=zz3O96ULg4nQMj2PurlTBZecedxhewhg; SPC_R_T_ID=381h9C7xlIhz0TP9YSDXmro/WaRDXA5bSVV704I/evi5gR4rxN9KLJpXGK6DJ7LgvISvN3uQyKyDiuq8Fs0TcNAhGC56FtL6KDa4dXJecY8tfxlZ/AtC85SjcMjjpflEPPv92h+oH+XtxHnWlzDvSUbXIsk+s/WXXJbVJVTSrjo=; SPC_R_T_IV=N3ppYVBuYWxaWDNJZmtkVQ==; SPC_SI=rBm8YgAAAABHUGV1bDBib2jXBQAAAAAAd0JzaXU4QTA=; SPC_T_ID=381h9C7xlIhz0TP9YSDXmro/WaRDXA5bSVV704I/evi5gR4rxN9KLJpXGK6DJ7LgvISvN3uQyKyDiuq8Fs0TcNAhGC56FtL6KDa4dXJecY8tfxlZ/AtC85SjcMjjpflEPPv92h+oH+XtxHnWlzDvSUbXIsk+s/WXXJbVJVTSrjo=; SPC_T_IV=N3ppYVBuYWxaWDNJZmtkVQ==',
            'Connection': 'close'
        }

        return self.headers

    @staticmethod
    def to_json(response):
        data = response.read()

        return json.loads(data.decode('utf-8'))

    def serialize(self):
        raise NotImplementedError
