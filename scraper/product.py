import requests

class Product:
    def __init__(self, link):
        self.link = link
        self.product_info_url = 'https://shopee.co.id/api/v4/item/get'
        self.product_rating_url = 'https://shopee.co.id/api/v2/item/get_ratings'

    def generate_headers(self):
        cookie = """SPC_IA=-1; SPC_EC=-; SPC_F=QpolQhTSikpnxRXO6T4RjIW8ZGHNBmBn; REC_T_ID=ac80cdde-0e7d-11e9-a8c2-3c15fb3af585; SPC_T_ID="e4t1VmH0VKB0NajA1BrHaDQlFRwWjTZT7o83rrHW+p16sTf1NJK7ksWWDicCTPq8CVO/S8sxnw25gNR0DLQz3cv7U3EQle9Z9ereUnPityQ="; SPC_SI=k2en4gw50emawx5fjaawd3fnb5o5gu0w; SPC_U=-; SPC_T_IV="in3vKQSBLhXzeTaGwMInvg==";_gcl_au=1.1.557205539.1546426854; csrftoken=8XtQ7bHlv09rlx5U4NPN6rmavFn7MvTO; welcomePkgShown=true; bannerShown=true; _ga=GA1.3.472488305.1546426857;_gid=GA1.3.1348013297.1546426857; _fbp=fb.2.1546436170115.11466858"""

        return {
            'accept-encoding': 'gzip, deflate, br',
            'accept': '*/*',
            'content-type': 'application/json',
            'if-none-match': '55b03-1ae7d4aa7c47753a96c0ade3a9ea8b35',
            'origin': 'https://shopee.co.id',
            'referer': self.link,
            'x-api-source': 'pc',
            'x-csrftoken': '8XtQ7bHlv09rlx5U4NPN6rmavFn7MvTO',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Thunder Client (https://www.thunderclient.com)',
            'cookie': cookie
        }

    # itemId and shopId is already exists in the url, we just need to extract it using some substring logic. Some regex may be used in the future.
    def get_shop_id(self):
        product_slug = str(self.link).split('/')[-1]
        return product_slug.split('.')[1]

    def get_item_id(self):
        product_slug = str(self.link).split('/')[-1].split('?')[0]
        return product_slug.split('.')[2]

    def valid_link(self):
        return self.link.startswith('https://shopee')

    def get_product_info_url(self):
        shop_id = self.get_shop_id()
        item_id = self.get_item_id()

        return f'{self.product_info_url}?itemid={item_id}&shopid={shop_id}'

    def get_product_rating_url(self, filter=0, limit=5):
        shop_id = self.get_shop_id()
        item_id = self.get_item_id()

        return f'{self.product_rating_url}?itemid={item_id}&shopid={shop_id}&filter={filter}&limit={limit}&offset=0&type=0'
        
    def get_product_info(self):
        if not self.valid_link():
            return None
        
        url = self.get_product_info_url()
        with requests.session() as session:
            response = session.get(url, headers=self.generate_headers())

        return response

    def info(self):
        self.data = self.get_product_info().json()
        self.error = self.data['error'] if self.data['error'] else None

        return self

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

if __name__ == '__main__':
    product = Product('https://shopee.co.id/DOMPET-DISIPLIN-Keuangan-Bulanan-Walet-Organizer-Dompet-Organizer-Dompet-pintar-i.21749933.7286427645?sp_atk=c0b0f4cb-98a9-40bc-8390-21f35361f32c&xptdk=c0b0f4cb-98a9-40bc-8390-21f35361f32c')
    product.get_product_info()