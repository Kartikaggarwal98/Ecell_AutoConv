#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import requests
import re
import random
import pprint
import apiai

def scrape_spreadsheet():
    sheet_id='1c-8Zx-g0USneS5X9bThXf0G-O_NvXV6gT_k3VYnSIjE'
    #sheet_id = '1EXwvmdQV4WaMXtL4Ucn3kwwhS1GOMFu0Nh9ByVCfrxk'
    url = 'https://spreadsheets.google.com/feeds/list/%s/od6/public/values?alt=json'%(sheet_id)

    resp = requests.get(url=url)
    data = json.loads(resp.text)
    arr =[]

    for entry in data['feed']['entry']:
        d = {}
        for k,v in entry.iteritems():
            if k.startswith('gsx'):
                key_name = k.split('$')[-1]
                d[key_name] = entry[k]['$t']

        arr.append(d)

    return arr
spreadsheet_object = scrape_spreadsheet()
item_arr = [i for i in spreadsheet_object if i['etype'] == 'members']
elements_arr = []

for i in item_arr:
    sub_item = {
                    "title":i['ename'],
                    "item_url":i['elink'],
                    "image_url":i['epicture'],
                    "buttons":[
                      {
                        "type":"web_url",
                        "url":i['elink'],
                        "title":"Open"
                      },
                      {
                        "type":"element_share"
                      }              
                    ]
                  }
    elements_arr.append(sub_item)
print elements_arr