from .base import BaseWrapper
from .review import ProductReview
from functools import cached_property

class Product(BaseWrapper):
    def __init__(self, link = None, shop_id = None, item_id = None, **kwargs):
        super().__init__()
        self.link = link
        self.shop_id = shop_id
        self.item_id = item_id
        self.kwargs = kwargs
        self.base_url = 'https://shopee.co.id/api/v4/item/get'

    @cached_property
    def reviews(self):
        return ProductReview(shop_id=self.shop_id, item_id=self.item_id, **self.kwargs)

    @cached_property
    def url(self):
        if not self.link and not (self.shop_id and self.item_id):
            raise Exception('link or shop_id and item_id is required')

        if self.link and not (self.shop_id and self.item_id):
            self.shop_id = self.__get_shop_id()
            self.item_id = self.__get_item_id()

        return f'{self.base_url}?itemid={self.item_id}&shopid={self.shop_id}'

    def __get_shop_id(self):
        product_slug = str(self.link).split('/')[-1]
        return product_slug.split('.')[1]

    def __get_item_id(self):
        product_slug = str(self.link).split('/')[-1].split('?')[0]
        return product_slug.split('.')[2]
    
    def __get_product_info(self):
        self.connection.request('GET', self.url, headers=self.headers)

        with self.connection.getresponse() as response:
            self.data = self.to_json(response)
            self.status_code = response.getcode()
            self.error = self.data['error'] if self.data['error'] else None

        return self.data

    def __serialize_variation_options(self, variation):
        if not self.data or self.error:
            return None

        result = []

        for index, option in enumerate(variation['options']):
            result.append({
                'name': option,
                'image': f'{self.image_base_url}/{variation["images"][index]}' if variation['images'] != None else None,
            })

        return result

    def __serialize_variations(self):
        if not self.data or self.error:
            return None

        result = []

        for variation in self.data['data']['tier_variations']:
            result.append({
                'name': variation['name'],
                'options': self.__serialize_variation_options(variation)
            })

        return result

    @cached_property
    def serialize(self):
        self.__get_product_info()
        if not self.data or self.error:
            return None

        return {
                'meta': {
                    'item_id': self.data['data']['itemid'],
                    'shop_id': self.data['data']['shopid'],
                    'user_id': self.data['data']['userid'],
                    'shopee_endpoint': self.url
                },
                'product': {
                    'name': self.data['data']['name'],
                    'description': self.data['data']['description'],
                    'brand': self.data['data']['brand'],
                    'price_min': self.data['data']['price_min'],
                    'price_max': self.data['data']['price_max'],
                    'price': self.data['data']['price'],
                    'discount': self.data['data']['discount'],
                    'sold': self.data['data']['sold'] if self.data['data']['sold'] > self.data['data']['historical_sold'] else self.data['data']['historical_sold'],
                    'stock': self.data['data']['stock'],
                    'like': self.data['data']['liked_count'],
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
                    'variations': self.__serialize_variations(),
                    'models': [
                        {
                            'item_id': model['itemid'],
                            'model_id': model['modelid'],
                            'tier_index': model['extinfo']['tier_index'],
                            'name': model['name'],
                            'price': model['price'],
                            'stock': model['stock']
                        } for model in self.data['data']['models']],
                    'attributes': self.data['data']['attributes'],
                    'categories': self.data['data']['categories'],
                    'images': [f'{self.image_base_url}/{image}' for image in self.data['data']['images']],
                    'videos': [
                        {
                            'id': video['video_id'],
                            'thumbnail': f'{self.image_base_url}/{video["thumb_url"]}',
                            'url': video['default_format']['url'],
                            'format': video['default_format']['profile'],
                            'definition': video['default_format']['defn']
                        } for video in self.data['data']['video_info_list']] if self.data['data']['video_info_list'] else None,
                }
            }