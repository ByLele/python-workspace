import os 
import pprint

import time
import json
from datetime import datetime, timedelta
import requests
class notionBase(object):
    def __init__(self):
        self.notion_token = self.notion_token()

    @classmethod
    def a(cls):
        pass
    @classmethod
    def notion_token(self):
        with open(".\\env.json") as f:
            r = json.load(f)
            print(r)
            if r.get("NOTION_KEY"):
                return True,r.get("NOTION_KEY")
            else:
                return False,"Get notoken failed"


def notion_token():
    with open(".\\env.json") as f:
        r = json.load(f)
        print(r)
        if r.get("NOTION_KEY"):
            return True, r.get("NOTION_KEY")
        else:
            return False, "Get notoken failed"
def notion_pageid():
    with open(".\\env.json") as f:
        r = json.load(f)
        print(r)
        if r.get("NOTION_PAGE_ID"):
            return True,r.get("NOTION_PAGE_ID")   
        else:
            return False,"Get npid failde"
        

def notion_page_detail(token,pageid):
    
    if not token or not pageid:
        print("paras ")
        return


    # API Endpoint
    endpoint = f"https://api.notion.com/v1/pages/{pageid}"

    # Headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16",  # or the version you're using
    }
    response = requests.get(endpoint, headers=headers)

    # Process the response
    if response.status_code == 200:
        page_data = response.json()
        properties = page_data.get('properties', {})
        print(properties)
    else:
        print(f"Error {response.status_code}: {response.text}")
    
def notion_page_additem(token,pageid,title,content):
    parent_database_id = pageid  # Replace with your database ID
    endpoint = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16",  # Use the version you're working with; check Notion's API documentation for the latest
        "Content-Type": "application/json"
    }
    
    today_str = datetime.now().strftime('%Y-%m-%d')

    # Define the request payload
# Request payload
    payload = {
        "parent": {"database_id": pageid},
        "properties": {
            "Name": {
                "title": [
                    {"text": {"content": title}}
                ]
            },
            "Date": {  # Assuming you have a date property named "Date"
                "date": {
                    "start": today_str
                }
            },
            # "Relation": {  # Assuming you have a relation property named "Relation"
            #     "relation": [
            #         {"id": pageid}
            #     ]
            # }
            "text":{
                "type":"text",
                "text":{"act":content}
            }
        }
    }


    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        print("Successfully added item 'a'")
    else:
        print(f"Error {response.status_code}: {response.text}")
    
    
    
if __name__ == "__main__":
    status,token = notion_token()
    print(status,token)
    #pageid = "780d7bfd44a64a37bcb21c5f5278053e"
    pageid = "780d7bfd44a64a37bcb21c5f5278053e"
    notion_page_additem(token=token,pageid=pageid,title=1,content=2)
    #notion_page_detail(token=token,pageid=pageid)
    