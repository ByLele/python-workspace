import requests
import datetime
import sys
from pprint import pprint
from notion_client import Client,AsyncClient
from notion_client.helpers import get_id
from logging import Logger
NOTION_TOKEN = "secret_fz8hGuVnnQsTbifpRhXx0SCAfNiqSSPBn7IGfZKh0ww"
DATABASE_ID =  "d983fecfb48940099d26ab138176a29f" #"780d7bfd44a64a37bcb21c5f5278053e"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

class App(object):
    def __init__(self) -> None:
        self.token = "secret_fz8hGuVnnQsTbifpRhXx0SCAfNiqSSPBn7IGfZKh0ww"
    @classmethod
    def new_client(cls,token):
        return Client(auth=token)
    
    def create_database(self,notion,parent_id:str,db_name:str)->dict:
        """
        parent_id(str): ID of the parent page
        db_name(str): Title of the database
        """
        print(f"\n\nCreate database '{db_name}' in page {parent_id}...")
        properties = {
            "Name": {"title": {}},  # This is a required property
            "Description": {"rich_text": {}},
            "In stock": {"checkbox": {}},
            "status group": {
                "select": {
                    "options": [
                        {"name": "🥦 finish", "color": "green"},
                        {"name": "🍎 no start", "color": "red"},
                        {"name": "💪 block", "color": "yellow"},
                    ]
                }
            },
            "publishAt": {"date":{}},
            "Last ordered": {"date": {}},
            "URL":{"rich_text":{}},
            "Store availability": {
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {"name": "eo", "color": "blue"},
                        {"name": "po", "color": "gray"},
                        {"name": "te", "color": "purple"},
                        {"name": "ot", "color": "yellow"},
                    ]
                },
            },
            "+1": {"people": {}},
            "Photo": {"files": {}},
        }
        title = [{"type": "text", "text": {"content": db_name}}]
        icon = {"type": "emoji", "emoji": "🎉"}
        parent = {"type": "page_id", "page_id": parent_id}
        return notion.databases.create(
            parent=parent, title=title, properties=properties, icon=icon
        )
    
    def db_add_col(self,notion,parent_id,title,desc,url,publishat)->dict:
                
        print(f"\n\ add database '{parent_id}' col..")
        properties = {
            "Name": {"title":[{ type: "text", "text": { "content": title } }]},  # This is a required property
            "Description": {"rich_text": {"content":desc}},
            "In stock": {"checkbox": {}},
            "URL": {"rich_text": {"content":url}},
            "status group": {
                "select": {"name": "🍎 no start", "color": "red"}
            },
            "publishAt": {"date":{"start":publishat}},
            "Last ordered": {"date": {}},
            "URL":{"rich_text":{}},
            "Store availability": {
                "type": "multi_select",
                "multi_select": {"name": "po", "color": "gray"}},
            "+1": {"people": {}},
            "Photo": {"files": {}},
        }
        parent = {"type": "database_id", "database_id": parent_id}
        return notion.databases.update(
            databae_id="90cc1a489ec14a78ae14a8de4abcabb7", properties=properties
        )



def db_info():
    
    notion = Client(auth=NOTION_TOKEN)  # 替换为自己的Token
    db_name = "New database name"    # 替换为自己的DataBase名称
    db_id = "f584eb54-7877-44f0-8c15-29f9551c1ce5"    # 替换为自己的DataBase ID
    page_id = "317cdbedcd35469c90b4854fe3f053d7"   # # 替换为自己的Page ID

    # notion.search 搜索指定对象是否存在
        # query 指定搜索对象：database的 db_id、db_name
        # filter 是筛选条件，其中属性为"object"对象，值可以是"database"，也可以是"page"
    results = notion.search(query=db_name, filter={"property": "object", "value": "database"}).get("results")
    pprint(results)
    print(type(results))    # 返回类型为list列表
    #pprint(results)
    if (results is None) or (len(results) == 0):
        print(f"Notion中找不到DataBase【{db_name}】")
    else:
        db_id = results[0]["id"]   # 找到列表第一组字典中键名“id"的值
        print(db_id)
        print(f"Notion中存在DataBase【{db_name}】")

    # notion.databases.retrieve() 获取指定数据库db_id信息，返回数据库信息的对象为'列名'及'列属性'，但不包括'列值'。
    db_info = notion.databases.retrieve(database_id=db_id)  
    print(type(db_info))    # 返回类型为dict字典
    pprint(db_info) 

    # notion.databases.query() 查询指定数据库db_id的所有记录，返回包含所有符合筛选条件的记录列表，包括'列名'、'列属性'、'列值'。可批量获取数据，进行筛选和排序操作，适用于处理大批量数据。
    db_values = notion.databases.query(database_id=db_id).get("results")
    pprint(type(db_values))   # 返回类型为list列表
    pprint(db_values)   # 



if __name__ == "__main__":
    app = App()
    notion = app.new_client(token=app.token)
    pg_id = "317cdbedcd35469c90b4854fe3f053d7"
    #res = app.create_database(notion=notion,parent_id=pg_id,db_name="YT databases")
    
    parent = "90cc1a489ec14a78ae14a8de4abcabb7"
    
    res = app.db_add_col(notion=notion,parent_id=parent ,title="dfafadfasfd",desc="aaaa",url="http://localhost",publishat="aaa")
    pprint(res)