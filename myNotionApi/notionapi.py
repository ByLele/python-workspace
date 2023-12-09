import  os
import json
from datetime import datetime, timedelta
import requests
from pprint import pprint



from utils.notion_util import _json
from myNotionApi.uper_data_reader import uper_data_obj


class notionBase(object):
    def __init__(self):
        self.notion_token = self.notion_token()

    @classmethod
    def a(cls):
        pass
    @classmethod
    def notion_token(self):
        with open("../env.json") as f:
            r = json.load(f)
            print(r)
            if r.get("NOTION_KEY"):
                return True,r.get("NOTION_KEY")
            else:
                return False,"Get notoken failed"


def notion_token():
    with open("../env.json") as f:
        r = json.load(f)
        print(r)
        if r.get("NOTION_KEY"):
            return True, r.get("NOTION_KEY")
        else:
            return False, "Get notoken failed"
def notion_pageid():
    with open("../env.json") as f:
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
    
def notion_page_additem(token,pageid,title=None,content=None):
    parent_database_id = pageid  # Replace with your database ID
    endpoint = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16",  # Use the version you're working with; check Notion's API documentation for the latest
        "Content-Type": "application/json"
    }
    
    today_str = datetime.now().strftime('%Y-%m-%d')


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
            'Text': {'id': 'K%40tv',
                          'rich_text': [{'annotations': {'bold': False,
                                                         'code': False,
                                                         'color': 'default',
                                                         'italic': False,
                                                         'strikethrough': False,
                                                         'underline': False},
                                         'href': None,
                                         'plain_text': 'this is a test ',
                                         'text': {'content': content,
                                                  'link': None},
                                         'type': 'text'}],
                          'type': 'rich_text'}
        }
    }


    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        print("Successfully added item 'a'")
    else:
        print(f"Error {response.status_code}: {response.text}")
    
def notion_block_add(token,blockid,title,content):
    
    endpoint = "https://api.notion.com/v1/pages"  #f"https://api.notion.com/v1/{blockid}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16",  # Use the version you're working with; check Notion's API documentation for the latest
        "Content-Type": "application/json"
    }
    today_str = datetime.now().strftime('%Y-%m-%d')
    payload = {
	"parent": { "database_id": blockid },
	"properties": {
		"title": {
      "title": [{ "type": "text", "text": { "content": title } }]
		},
        "Date": {  # Assuming you have a date property named "Date"
                "date": {
                    "start": today_str,
                }
            },
	},
	"children": [
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{ "type": "text", "text": { "content": content } }]
      }
    }
  ]
}
    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        print("Successfully added item 'a'")
    else:
        print(f"Error {response.status_code}: {response.text}")
        


#add uper to a database
def notion_database_add(token,parentid):
    
    endpoint = "https://api.notion.com/v1/pages"#f"https://api.notion.com/v1/databases/{parentid}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16",  # Use the version you're working with; check Notion's API documentation for the latest
        "Content-Type": "application/json"
    }
    today_str = datetime.now().strftime('%Y-%m-%d')

    payload = {
    "parent": {
      "type": "database_id",
      "database_id": parentid,
    },
    "properties": {
        "UP": {
            "title":[{"text":{"content":"tomato"} }]
        },
        "news": {
            "text": {"content":"aaaaaaaaaaaaaaa"}
        },
        "Last ordered": {
            "date": {"date":today_str}
        },

    },

}
    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        print("Successfully added createbase 'a'")
    else:
        print(f"Error {response.status_code}: {response.text}")



def readDatabase(databaseID, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseID}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
        # print(res.text)

    with open('../full-properties.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)
    return data

def db_add_page(databaseID, headers,properties):

    data = {
    "parent": {
      "database_id": databaseID,
    },
    "properties": properties,
  }
    readUrl = "https://api.notion.com/v1/pages"
    res = requests.request("POST", readUrl, headers=headers,json=data)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    return data




if __name__ == "__main__":
    # status,token = notion_token()
    # print(status,token)
    # #pageid = "780d7bfd44a64a37bcb21c5f5278053e"
    # pageid = "780d7bfd44a64a37bcb21c5f5278053e" #ps test page
    # #notion_block_add(token=token,blockid=pageid,title="11.17",content="1717171717171717171")
    # pageid = "e7ef2f6346d44a48a012c487500243d4"
    # pageid = "e217cac1b34241b0ab324e271fd5e4d7"
    # pageid = "9234a7bc1ee74b7e8de917da5783179c"
    # notion_database_add(token=token,parentid=pageid)

    token = 'secret_fz8hGuVnnQsTbifpRhXx0SCAfNiqSSPBn7IGfZKh0ww'
    databaseID = "90cc1a489ec14a78ae14a8de4abcabb7"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }

    #res = readDatabase(databaseID=databaseID,headers=headers)

    #pprint(res)
    ppp = {'+1': {'type': 'people',
        'people': [],
        },
        'Description': {
                                             'rich_text': [{'annotations': {'bold': False,
                                                                            'code': False,
                                                                            'color': 'default',
                                                                            'italic': False,
                                                                            'strikethrough': False,
                                                                            'underline': False},
                                                            'href': None,
                                                            'text': {'content': 'this is desc',
                                                                     'link': None},
                                                            'type': 'text'}],
                                             'type': 'rich_text'},
        'In stock': {'checkbox': False,
                                          'type': 'checkbox'},
        'Last ordered': {'date': None,
                                              'type': 'date'},
        'Name': {'title': [{'annotations': {'bold': False,
                                                                 'code': False,
                                                                 'color': 'default',
                                                                 'italic': False,
                                                                 'strikethrough': False,
                                                                 'underline': False},
                                                 'href': None,
                                                 'text': {'content': '2222222222222',
                                                          'link': None},
                                                 'type': 'text'}],
                                      'type': 'title'},
        'Photo': {'files': [],
                                       'type': 'files'},
        'Store availability': {
                                                    'multi_select': [{'color': 'blue',
                                                                      'id': '60f1bd37-f61c-4fd4-a1c3-5753dec4e266',
                                                                      'name': 'eo'},
                                                                     {'color': 'gray',
                                                                      'id': '0ddf221e-bc00-428a-ab61-19a7daedc51e',
                                                                      'name': 'po'}],
                                                    'type': 'multi_select'},
        'URL': {
                                     'rich_text': [{'annotations': {'bold': False,
                                                                    'code': False,
                                                                    'color': 'default',
                                                                    'italic': False,
                                                                    'strikethrough': False,
                                                                    'underline': False},
                                                    'href': None,
                                                    'plain_text': 'aaa',
                                                    'text': {'content': 'aaa',
                                                             'link': None},
                                                    'type': 'text'}],
                                     'type': 'rich_text'},
        'publishAt': {'date': {'end': None,
                                                    'start': '2023-12-05',
                                                    'time_zone': None},
                                           'type': 'date'},
        'status group': {
                                              'select': {'color': 'red',
                                                         'id': 'b1436b93-bed9-4593-b1b8-4d4228568df0',
                                                         'name': '🍎 no start'},
                                              'type': 'select'}}
    json_data = uper_data_obj
    _json(json_data,new_value="desc",json_path="$.Description.rich_text[0].text.content")
    _json(json_data,new_value="Name Title",json_path="$.Name.title[0].text.content",)
    _json(json_data,new_value="URL",json_path="$.URL.rich_text[0].text.content")
    _json(json_data,new_value= "2013-12-06", json_path="$.publishAt.date.start")


    pprint(json_data)

    res = db_add_page(databaseID=databaseID, headers=headers,properties=json_data)

    print(res)