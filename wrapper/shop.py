from .base import BaseWrapper
from .product import Product
from functools import cached_property

class Shop(BaseWrapper):
    def __init__(self, link=None, username=None):
        super().__init__()
        self.link = link
        self.username = username
        self.base_url = 'https://shopee.co.id/api/v4/shop/get_shop_detail'
        self.products_url = 'https://shopee.co.id/api/v4/shop/search_items'
        
        if link:
            self.__get_shop_username_from_link()
            self.__get_shop_info()
        elif username:
            self.__get_shop_info()
        else:
            raise ValueError('Either link or username is required')

    def __get_shop_username_from_link(self):
        self.username = self.link.split('/')[-1].split('.')[0]
        return self.username

    def __get_shop_info(self):
        url = f'https://shopee.co.id/api/v4/shop/get_shop_detail?&username={self.username}'
        self.connection.request('GET', url, headers=self.headers)

        with self.connection.getresponse() as response:
            self.data = self.to_json(response)
            self.status_code = response.getcode()
            self.error = self.data['error'] if self.data['error'] else None
            self.shop_id = self.data['data']['shopid'] if self.data['data'] else None

        return self.data

    @cached_property
    def products(self):
        # self.products_url = f'{self.products_url}?shopid={self.shop_id}&limit={self.serialize["item_count"]}'
        self.products_url = f'{self.products_url}?shopid={self.shop_id}&limit=5'
        self.connection.request('GET', self.products_url, headers=self.headers)
        print('ewe')

        with self.connection.getresponse() as response:
            data = self.to_json(response)
        
        if data['items']:
            return [Product(shop_id=item['shopid'], item_id=item['itemid']) for item in data['items']]

        return []

    @cached_property
    def serialize(self):
        if not self.data or self.error:
            return None

        return {
            'meta': {
                'user_id': self.data['data']['userid'],
                'shop_id': self.data['data']['shopid'],
            },
            'name': self.data['data']['name'],
            'description': self.data['data']['description'],
            'item_count': self.data['data']['item_count'],
            'country': self.data['data']['country'],
            'rating': {
                'average': self.data['data']['rating_star'],
                'rating_count': self.data['data']['rating_normal'] + self.data['data']['rating_good'] + self.data['data']['rating_bad'],
                'bad_rating_count': self.data['data']['rating_bad'],
                'good_rating_count': self.data['data']['rating_good'],
                'normal_rating_count': self.data['data']['rating_normal'],
            },
            'is_official_shop': self.data['data']['is_official_shop'],
            'is_shopee_verified': self.data['data']['is_shopee_verified'],
            'shop_location': self.data['data']['shop_location'],
            'shop_covers': [{'url': f'{self.image_base_url}/{cover["image_url"]}'} for cover in self.data['data']['shop_covers'] if cover['type'] == 0] if self.data['data']['shop_covers'] else None,
        }

class ShopProductProxy:
    def __init__(self, shop_id, item_id):
        self.shop_id = shop_id
        self.item_id = item_id
    
    @cached_property
    def serialize(self):
        product = Product(shop_id=self.shop_id, item_id=self.item_id)
        return product.serialize