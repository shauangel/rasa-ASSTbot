from . import config
import requests


def search_fetch_and_analysis(qkey):
    # Step 1. Search via Custom JSON Search API
    result_page = requests.post(url=config.TOOLBOX_URL + "/api/search",
                                json={"keywords": qkey,
                                      "result_num": 10,
                                      "page_num": 0})
    # Step 2. Fetch data
    stack_items = requests.post(url=config.TOOLBOX_URL + "/SO_api/get_items",
                                json={"urls": result_page['result']})
    # Step 3. block analysis
    resp = requests.post(url=config.TOOLBOX_URL + "/api/block_analysis",
                         json={"items": stack_items['items']})
    return resp['rank'], stack_items['items']
