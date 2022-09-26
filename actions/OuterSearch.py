#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 00:31:47 2021

@author: linxiangling
"""

#輸入參數關鍵字string array、一次需回傳筆數、第幾頁
def outerSearch(keyWords, resultNum, pageNum):
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
    
    separator = " "
    #to search
    query = separator.join(keyWords) + " site:stackoverflow.com"
    #Test
    #for i in search(query, tld = "com", num = resultNum, start = resultNum * pageNum,stop = resultNum, pause = 0.1):
    #    print(i)
    return [i for i in search(query, tld = "com", num = resultNum, start = resultNum * pageNum,stop = resultNum, pause = 0.1)]
    
#pause (float) – Lapse to wait between HTTP requests. A lapse too long will make the search slow, but a lapse too short may cause Google to block your IP. Your mileage may vary!

#Test
#ouserSearch(['flask', 'CORS', 'error'], 10, 0)
