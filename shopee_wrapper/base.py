import http.client
import json

class BaseWrapper:
    base_url = 'https://shopee.co.id'
    image_base_url = 'https://cf.shopee.co.id/file'
    video_base_url = 'http://play-ws.vod.shopee'
    status_code = 200
    error = None

    def __init__(self):
        self.establish_connection()
        self.generate_headers()

    def establish_connection(self):
        self.connection = http.client.HTTPSConnection('shopee.co.id')

        return self.connection

    def generate_headers(self):
        self.headers = {
            'Cookie': 'REC_T_ID=6bab0c7a-f8f1-11ec-a247-2cea7f4774b9; SPC_F=zz3O96ULg4nQMj2PurlTBZecedxhewhg; SPC_R_T_ID=381h9C7xlIhz0TP9YSDXmro/WaRDXA5bSVV704I/evi5gR4rxN9KLJpXGK6DJ7LgvISvN3uQyKyDiuq8Fs0TcNAhGC56FtL6KDa4dXJecY8tfxlZ/AtC85SjcMjjpflEPPv92h+oH+XtxHnWlzDvSUbXIsk+s/WXXJbVJVTSrjo=; SPC_R_T_IV=N3ppYVBuYWxaWDNJZmtkVQ==; SPC_SI=rBm8YgAAAABHUGV1bDBib2jXBQAAAAAAd0JzaXU4QTA=; SPC_T_ID=381h9C7xlIhz0TP9YSDXmro/WaRDXA5bSVV704I/evi5gR4rxN9KLJpXGK6DJ7LgvISvN3uQyKyDiuq8Fs0TcNAhGC56FtL6KDa4dXJecY8tfxlZ/AtC85SjcMjjpflEPPv92h+oH+XtxHnWlzDvSUbXIsk+s/WXXJbVJVTSrjo=; SPC_T_IV=N3ppYVBuYWxaWDNJZmtkVQ==',
            'Connection': 'close',
            'AF-AC-ENC-DAT': 'AAcyLjUuMi0yAAABhdbDaGQAAAzeAoAAAAAAAAAAAiS4mTYXtBIM3/aVutv7vv95BRd698jZ/901tpYwiYTjGF/2xGLP3PvqXW8MCO4GZjd0LOP5ucxzA6P+HlxI8a0e0EITl/82EyfDx/bVRcPaaRvYm0iAHc9YPNN3N+N4xKMBpujmZ7VFnAs5HbXqfjiMTh5Wl/82EyfDx/bVRcPaaRvYm7Q7Y7iER0YZDuPlzDCijEDdpMsZ74BuVdOliab30GDtvsGH5bvVcZqN1VGQ/nuCwUpbg/iduB+irk6FJ69PY+1fOBbJvLvYAVLMa+wqKcDPO/6faKm+ZVKsH4uNXJ5E7ppLBWCjreCQPoeLs2qGai1PXjEGGWy3DMVVukZKDs+2mB2ojoppDRDE4m+SQNZ5dTPdxAi7ISkMhAiEVo9TfIv6D60EAfL6N+xglYXjLTEDPHwai1Hpp02msuwKPRyHq7M79uFmkEeSIzznOECBsA1WP5bOtSjQMliLPHU49jrTIPznogusS6HG56/Ud4S2QU0ah2EGVFJ6qY6RA65n+hoQ93OHsMtIrOd1VgYAe4oU/t4Mua5+k/FLRe4WuevGICG019hD/ZVAy6L8CRUdBtFHZYe7jrVGRDP+TMtRKgf3r9BOlMHgrMoCBnXxFjDEyCgFa119bbLTGYa9RFB4bXC1BnYf0sH6Fd3QTyiHd8Keybp71S0T2mIq5wg4Hh3ayt22wZu1fv5e3dGER2nDn0Gy4FawdTAEX7UzbO9sQyW4bh5jEx88pTZkjBaE0hpNb7DrFa8fe4xhhZ0urMpOtyzV+h2R+es0bAdJ0P1V6oB+MKkk05uyBi99RpxpITDk9Nrht2CSin9letnhWPkJTMuoAJjhjlGFNhnzHRlHxeSi',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        return self.headers

    @staticmethod
    def to_json(response):
        data = response.read()

        return json.loads(data.decode('utf-8'))

    def serialize(self):
        raise NotImplementedError
