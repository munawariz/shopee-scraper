from .base import BaseWrapper

class Shop(BaseWrapper):
    def __init__(self, link=None, username=None):
        super().__init__()
        
        if link:
            self.shop_id = self.__get_shop_id_from_link(link)
        elif username:
            self.shop_id = self.__get_shop_id_from_username(username)
        else:
            raise ValueError('Either link or username is required')

    def __get_shop_id_from_link(self):
        raise NotImplementedError

    def __get_shop_id_from_username(self):
        raise NotImplementedError

    def __get_shop_info(self):
        raise NotImplementedError

    def __get_products_from_shop(self):
        raise NotImplementedError

    def serialize(self):
        return super().serialize()
