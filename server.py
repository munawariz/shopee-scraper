from fastapi import FastAPI, Request, Response, Body
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from wrapper import Product, ProductReview, Shop

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
    return RedirectResponse(url='/docs', status_code=302)

@app.get("/shops/")
async def get_shop(request: Request, response: Response, payload: dict = Body(default={})):
    url = payload['url'] if 'url' in payload else request.query_params.get('url')
    username = payload['username'] if 'username' in payload else request.query_params.get('username')
    shop = Shop(link=url, username=username)

    response.status_code = shop.status_code
    response.body = shop.serialize() if not shop.error else {'error': shop.error}
    return response.body

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
