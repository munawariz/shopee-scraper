from .base import BaseWrapper

class Product(BaseWrapper):
    def __init__(self, link):
        super().__init__()
        self.link = link
        self.base_url = 'https://shopee.co.id/api/v4/item/get'
        self.data = self.__get_product_info()

    # itemId and shopId is already exists in the url, we just need to extract it using some substring logic. Some regex may be used in the future.
    def get_shop_id(self):
        product_slug = str(self.link).split('/')[-1]
        return product_slug.split('.')[1]

    def get_item_id(self):
        product_slug = str(self.link).split('/')[-1].split('?')[0]
        return product_slug.split('.')[2]

    def get_product_info_url(self):
        self.shop_id = self.get_shop_id()
        self.item_id = self.get_item_id()
        return f'{self.base_url}?itemid={self.item_id}&shopid={self.shop_id}'
        
    def __get_product_info(self):
        if not self.valid_link():
            return None
        
        url = self.get_product_info_url()
        self.connection.request('GET', url, headers=self.headers)

        with self.connection.getresponse() as response:
            self.data = self.to_json(response)
            self.status_code = response.getcode()
            self.error = self.data['error'] if self.data['error'] else None

        return self.data

    def serialize(self):
        if not self.data or self.error:
            return None

        return {
                'meta': {
                    'item_id': self.data['data']['itemid'],
                    'shop_id': self.data['data']['shopid'],
                    'user_id': self.data['data']['userid']
                },
                'product': {
                    'name': self.data['data']['name'],
                    'description': self.data['data']['description'],
                    'price_min': self.data['data']['price_min'],
                    'price_max': self.data['data']['price_max'],
                    'price': self.data['data']['price'],
                    'sold': self.data['data']['sold'] if self.data['data']['sold'] > self.data['data']['historical_sold'] else self.data['data']['historical_sold'],
                    'rating': {
                        'average': self.data['data']['item_rating']['rating_star'],
                        'count': self.data['data']['item_rating']['rating_count'][0],
                        'star': {
                            '1': self.data['data']['item_rating']['rating_count'][1],
                            '2': self.data['data']['item_rating']['rating_count'][2],
                            '3': self.data['data']['item_rating']['rating_count'][3],
                            '4': self.data['data']['item_rating']['rating_count'][4],
                            '5': self.data['data']['item_rating']['rating_count'][5],
                        }
                    },
                    'attributes': self.data['data']['attributes'],
                    'categories': self.data['data']['categories'],
                }
            }
