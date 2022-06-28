import json
import requests

class ShopeeScrapper:
    def __init__(self, username):
        self.username = username
    
    def scrape_list_items(self):
        req = requests.session()
        user_id, error_msg = self.get_user_id(self.username, req)
        return self.get_products(user_id, req), error_msg

    def generate_items_json(self, products):
        data = []
        for product in products:
            product = product['item_basic']
            json_data = {}
            json_data['id'] = product['itemid']
            json_data['name'] = product['name']
            json_data['price'] = product['price']/100000
            json_data['sold'] = product['historical_sold']
            json_data['rating'] = product['item_rating']['rating_star']
            json_data['rating_count'] = product['item_rating']['rating_count'][0]
            data.append(json_data)
        return data

    def get_request_headers(self):
        cookie = """SPC_IA=-1; SPC_EC=-; SPC_F=QpolQhTSikpnxRXO6T4RjIW8ZGHNBmBn; REC_T_ID=ac80cdde-0e7d-11e9-a8c2-3c15fb3af585; SPC_T_ID="e4t1VmH0VKB0NajA1BrHaDQlFRwWjTZT7o83rrHW+p16sTf1NJK7ksWWDicCTPq8CVO/S8sxnw25gNR0DLQz3cv7U3EQle9Z9ereUnPityQ="; SPC_SI=k2en4gw50emawx5fjaawd3fnb5o5gu0w; SPC_U=-; SPC_T_IV="in3vKQSBLhXzeTaGwMInvg==";_gcl_au=1.1.557205539.1546426854; csrftoken=8XtQ7bHlv09rlx5U4NPN6rmavFn7MvTO; welcomePkgShown=true; bannerShown=true; _ga=GA1.3.472488305.1546426857;_gid=GA1.3.1348013297.1546426857; _fbp=fb.2.1546436170115.11466858"""

        return {
            "accept-encoding": "gzip, deflate, br",
            "accept": "*/*",
            "content-type": "application/json",
            "if-none-match": "55b03-1ae7d4aa7c47753a96c0ade3a9ea8b35",
            "origin": "https://shopee.co.id",
            "referer": "https://shopee.co.id/macamacarons",
            "x-api-source": "pc",
            "x-csrftoken": "8XtQ7bHlv09rlx5U4NPN6rmavFn7MvTO",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Thunder Client (https://www.thunderclient.com)",
            "cookie": cookie
        }

    def get_user_id(self, username, req):
        headers = self.get_request_headers()
        url = f"https://shopee.co.id/api/v4/shop/get_shop_detail?sort_sold_out=0&username={username}"
        result = req.get(url, headers=headers)
        data = result.json()
        user_id = data['data']['shopid'] if data['data'] else None
        return user_id, data['error_msg']
    
    def get_products(self, user_id, req):
        headers = self.get_request_headers()
        
        if user_id:
            url = f'https://shopee.co.id/api/v4/search/search_items?by=pop&limit=30&match_id={user_id}&newest=0&only_soldout=1&order=desc&page_type=shop&scenario=PAGE_OTHERS&version=2'
            result = req.get(url, headers=headers)
            data = result.json()
            return data['items'] if not data['error'] else []
        return []

    def save_to_json(self, user_id, products):
        data = []
        for product in products:
            product = product['item_basic']
            json_data = {}
            json_data['id'] = product['itemid']
            json_data['name'] = product['name']
            json_data['price'] = product['price']/100000
            json_data['sold'] = product['historical_sold']
            json_data['rating'] = product['item_rating']['rating_star']
            json_data['rating_count'] = product['item_rating']['rating_count'][0]
            data.append(json_data)
        
        file_name = f'Shopee_{user_id}.json'
        with open(file_name, 'w') as file:
            json.dump(data, file)
