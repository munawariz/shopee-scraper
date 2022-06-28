from email import charset
from itertools import product
import string
from typing import Union
from fastapi import FastAPI
from shopee_scraper import *

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{username}")
async def read_items(username: str, q: Union[str, None] = None):
    shopee_scrapper = ShopeeScrapper(username)
    products, error_msg = shopee_scrapper.scrape_list_items()
    data = {}
    if not error_msg: data['data'] = shopee_scrapper.generate_items_json(products)
    data['message'] = error_msg
    return data