from typing import Union
from fastapi import FastAPI, Request, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from wrapper import Product, ProductReview
from shopee_scraper import *

app = FastAPI(title='shopee-wrapper', openapi_url=f'/shopee-wrapper/openapi.json')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

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

@app.get("/products/")
async def get_product(request: Request, response: Response, payload: dict = Body(default={})):
    url = payload['url'] if 'url' in payload else request.query_params.get('url')
    product = Product(url)

    response.status_code = product.status_code
    response.body = product.serialize() if not product.error else {'error': product.error}
    return response.body

@app.get("/reviews/")
async def get_review(request: Request, response: Response, payload: dict = Body(default={})):
    url = payload['url'] if 'url' in payload else request.query_params.get('url')
    filter = request.query_params.get('filter') or 0
    limit = request.query_params.get('limit') or 5
    offset = request.query_params.get('offset') or 0
    review = ProductReview(url, filter, limit, offset)

    response.status_code = review.status_code
    response.body = review.serialize() if not review.error else {'error': review.error}
    return response.body
