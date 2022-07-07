from .base import BaseWrapper
from functools import cached_property

class ProductReview(BaseWrapper):
    def __init__(self, link=None, shop_id=None, item_id=None, filter=0, limit=5, offset=0):
        super().__init__()
        self.link = link
        self.shop_id = shop_id
        self.item_id = item_id
        self.filter = filter
        self.limit = limit
        self.offset = offset
        self.base_url = 'https://shopee.co.id/api/v2/item/get_ratings'
        self.image_base_url = 'https://cf.shopee.co.id/file'

        self.data = self.__get_product_review()

    @cached_property
    def url(self):
        if not self.link and not (self.shop_id and self.item_id):
            raise Exception('link or shop_id and item_id is required')

        if self.link and not (self.shop_id and self.item_id):
            self.shop_id = self.__get_shop_id()
            self.item_id = self.__get_item_id()

        return f'{self.base_url}?itemid={self.item_id}&shopid={self.shop_id}&filter={self.filter}&limit={self.limit}&offset={self.offset}&type=0'

    def __get_product_review(self):
        self.connection.request('GET', self.url, headers=self.headers)

        with self.connection.getresponse() as response:
            self.data = self.to_json(response)
            self.status_code = response.getcode()
            self.error = self.data['error'] if self.data['error'] else None

        return self.data

    def __serialize_review(self):
        response = []
        for rating in self.data['data']['ratings']:
            rating_data = {
                'item_id': rating['itemid'],
                'user_id': rating['userid'],
                'username': rating['author_username'],
                'comment': rating['comment'],
                'created_at': rating['ctime'],
                'like_count': rating['like_count'],
                'images': [f'{self.image_base_url}/{image}' for image in rating['images']],
                'videos': [{'cover': video['cover'], 'url': video['url']} for video in rating['videos']],
                'tags': rating['tags'],
                'rating_star': rating['rating_star'],
            }
            response.append(rating_data)
        return response

    @cached_property
    def serialize(self):
        if not self.data or self.error:
            return None

        return {
            'meta': {
                'total': self.data['data']['item_rating_summary']['rating_total'],
                'with_media': self.data['data']['item_rating_summary']['rcount_with_media'],
                'with_context': self.data['data']['item_rating_summary']['rcount_with_context']
            },
            'reviews': self.__serialize_review()
        }
