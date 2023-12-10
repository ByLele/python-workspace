# *utf-8*
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
import urllib.parse as p
import re
import os
import pickle
import pprint
import json
import yaml
import sys
import time
from loguru import logger
sys.path.append("/Users/vbnvc/GitRepo/python-workspace")
from utils.notion_util import _json                                                                                             
from myNotionApi.uper_data_reader import uper_data_obj
from myNotionApi.notionapi import db_add_page
from utils.logger_util import logger
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
token = 'secret_fz8hGuVnnQsTbifpRhXx0SCAfNiqSSPBn7IGfZKh0ww'
databaseID = "90cc1a489ec14a78ae14a8de4abcabb7"
headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }
    

def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    #client_secrets_file = "./client_secret_523219218819-cjaggat5t7bkju2m4ss1e6lge2c8calu.apps.googleusercontent.com.json"
    #client_secrets_file = "./client_hgfcbn_secret_847585282559-3j95bf9plmbcij3csa1dg2penimmntpc.apps.googleusercontent.com.json"
    client_secrets_file = "./client_secret_847585282559-2v2nh29jlgrhghibmma96suoleqfkek8.apps.googleusercontent.com.json"
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token5.pickle"):
        with open("token5.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token5.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)


def get_video_id_by_url(url):
    """
    Return the Video ID from the video `url`
    """
    # split URL parts
    parsed_url = p.urlparse(url)
    # get the video ID by parsing the query of the URL
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")
    
    
def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="snippet,contentDetails,statistics",
        **kwargs
    ).execute()
    
    
    
def get_sub(youtube,**kwargs):
    return youtube.subscriptions().list(
        part="snippet",
        #mySubscribers=True,
        mine=True,
        maxResults=50,
        **kwargs
    ).execute()


def uper_yaml_write(uper_data:dict) -> None:
    
    if len(uper_data) ==  0:
        logger.info()

    for item in uper_data:
        #pprint.pprint(item)

        filename = item.get("snippet").get("title")
        # json_data = json.dumps(item,enco,ensure_ascii=False)
        uper_data = {}
        uper_data["author"] = filename
        uper_data["kind"] = item.get("kind")
        uper_data["etag"] = item.get("etag")
        uper_data["snippet"] = item.get("snippet")

        
        print(filename)
        filename = filename +".yaml"
        filename = "./uper/"+filename 
        try:
            print(filename)
            with open(filename,"w",encoding='utf-8') as f:
                yaml.dump(uper_data,f,allow_unicode=True)
        except Exception as e:
            print(e)
        print("\n \n")
        

def yaml_reader(filepath: str) -> None:
    channelId = []
    for root, dirs, files in os.walk(filepath):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, "r") as f:
                    yaml_data = yaml.safe_load(f)
                    print(yaml_data)
                    if 'snippet' in yaml_data and 'channelId' in yaml_data['snippet']['resourceId']:
                        channel_id = yaml_data['snippet']['resourceId']['channelId']
                        channelId.append(channel_id)
            except yaml.YAMLError as exc:

                print(f"Error reading {file_path}: {exc}")
    logger.info("channelId read success")
    return channelId

  
def activity_channel_list(youtube,channelId:str,**kwargs):
    return youtube.activities().list(
        part="snippet",
        channelId=channelId,
        **kwargs
    ).execute()     

def uper_activities(youtube,channelId:str)-> dict:

    try:
        res = activity_channel_list(youtube=youtube,channelId=channelId)

        page_nexttoken = res.get("nextPageToken")
        activities_list = res.get("items",[])
        uper_activities = {}
        if len(activities_list) < 0:
            logger.info("no activities")
        uper_activities["uper"] = activities_list[0]["snippet"].get("channelTitle","")
        act_list = []
        title = []
        for item in activities_list:
            if item["snippet"].get("title") in title:
                continue
            if item["snippet"].get("type") != "upload":
                continue
            
            title.append(item["snippet"].get("title"))
        
            date_string = item["snippet"].get("publishedAt")
            date_string = date_string[:10]  
            upload={
                "title":item["snippet"].get("title"),
                "description":item.get("snippet").get("description"),
                "url":item["snippet"]["thumbnails"]["default"]["url"],
                "publishedAt":date_string
            }

            act_list.append(upload) 
            
        uper_activities['video_list'] = act_list
        return uper_activities
    except Exception as e:
        logger.error("activity_channel error")

def sub_sync(youtube):
        
    channellist = get_sub(youtube)
    items = channellist.get("items")
    uper_yaml_write(items)
    logger.info("uper folder sync sub data ")
    while channellist.get("nextPageToken"):
        
        channellist = get_sub(youtube,pageToken=channellist.get("nextPageToken"))
        items = channellist.get("items")
        uper_yaml_write(items)
    logger.info("sync_sub write yaml success")

def notion_sync(uper:dict):
    if uper and uper.get("uper") and uper.get("video_list"):
        
        
        video_list = uper.get("video_list") 
        uper = uper.get("uper")
        json_data = uper_data_obj
        for item in video_list:  
            
            _json(json_data,new_value=item.get("title",""),json_path="$.Description.rich_text[0].text.content")
            _json(json_data,new_value=uper,json_path="$.Name.title[0].text.content",)
            _json(json_data,new_value=item.get("url"),json_path="$.URL.rich_text[0].text.content")
            _json(json_data,new_value= item.get("publishedAt"), json_path="$.publishAt.date.start")

            print(json_data)

            res = db_add_page(databaseID=databaseID, headers=headers,properties=json_data)

            print(res)


def main():
    youtube = youtube_authenticate() 
    sub_sync(youtube=youtube)

    res = yaml_reader("./uper")
    if not res:
        logger.error("yaml_reader channelid None")
        return

    for item in res:
        uper_act = uper_activities(youtube=youtube,channelId=item)
        time.sleep(100)
        notion_sync(uper=uper_act)

if __name__ == "__main__":
        # authenticate to YouTube API
    # youtube = youtube_authenticate() 
    # video_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw&ab_channel=jawed"
    # # parse video ID from URL
    # video_id = get_video_id_by_url(video_url)
    # # make API call to get video info
    # response = get_video_details(youtube, id=video_id)
    # youtube = youtube_authenticate() 
    # sub_sync(youtube=youtube)

    # res = yaml_reader("./uper")
    # print(res)

    main()