from .base import BaseWrapper

class Shop(BaseWrapper):
    def __init__(self, link=None, username=None):
        super().__init__()
        self.link = link
        self.username = username
        self.base_url = 'https://shopee.co.id/api/v4/shop/get_shop_detail'
        
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

    def __get_products_from_shop(self):
        raise NotImplementedError

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
            'shop_covers': [{'url': f'{self.image_base_url}/{cover["image_url"]}'} for cover in self.data['data']['shop_covers'] if cover['type'] == 0],
        }
