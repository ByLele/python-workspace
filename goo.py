# *utf-8*
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import urllib.parse as p
import re
import os
import pickle
import pprint
import json
import yaml
import sys
from notionapi import notion_token,notion_page_additem
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console handler
    ]
)

# Create a logger object
logger = logging.getLogger(__name__)
def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    #client_secrets_file = "./client_secret_523219218819-cjaggat5t7bkju2m4ss1e6lge2c8calu.apps.googleusercontent.com.json"
    client_secrets_file = "./client_hgfcbn_secret_847585282559-3j95bf9plmbcij3csa1dg2penimmntpc.apps.googleusercontent.com.json"
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token3.pickle"):
        with open("token3.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token3.pickle", "wb") as token:
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
        
        
def yaml_reade(filepath:str)->None:
    for root,dir,file in os.walk(filepath):
        try:
            with open(file,"r") as f:
                yaml_data = yaml.safe_load(file)
        except Exception as e:
            print(e)
  
def activity_channel_list(channelId:str,**kwargs):
    return youtube.activities().list(
        part="snippet",
        channelId=channelId,
        **kwargs
    ).execute()     

def uper_activities(channelId:str)-> dict:
    res = activity_channel_list(channelId=channelId)
    
    page_nexttoken = res.get("nextPageToken")
    activities_list = res.get("items",[])
    uper_activities = {}
    if len(activities_list) < 0:
        logger.info("no activities")
    uper_activities["uper"] = activities_list[0]["snippet"].get("channelTitle","")
    act_list = []
    act = []
    title = []
    for item in activities_list:
        if item["snippet"].get("title") in title:
            continue
        if item["snippet"].get("type") != "upload":
            continue
        title.append(item["snippet"].get("title"))
        act.append({"title":item["snippet"].get("title")})
        act.append({"description":item.get("snippet").get("description")})
        act.append({"url":item["snippet"]["thumbnails"]["default"]["url"]})
        act.append({"time":item["snippet"].get("publishedAt")})
        act_list.append(act)  
          
    uper_activities['video_list'] = act_list
    return uper_activities

def notion_sync(uper:dict):
    pass
    
if __name__ == "__main__":
        # authenticate to YouTube API
    youtube = youtube_authenticate() 
    video_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw&ab_channel=jawed"
    # parse video ID from URL
    video_id = get_video_id_by_url(video_url)
    # make API call to get video info
    response = get_video_details(youtube, id=video_id)
    
    #pprint.pprint(response)
    
    # channellist = get_sub(youtube)
    # items = channellist.get("items")
    # uper_yaml_write(items)
    # while channellist.get("nextPageToken"):
        
    #     channellist = get_sub(youtube,pageToken=channellist.get("nextPageToken"))
    #     items = channellist.get("items")
    #     uper_yaml_write(items)
        

    # print(channellist)
    # print(channellist.items())
    # print("="*20)




    res = activity_channel_list(channelId="UCJncdiH3BQUBgCroBmhsUhQ")
    
    #pprint.pprint(res)
    
    page_nexttoken = res.get("nextPageToken")
    activities_list = res.get("items",[])
    uper_activities = {}
    if len(activities_list) < 0:
        logger.info("no activities")
    uper_activities["uper"] = activities_list[0]["snippet"].get("channelTitle","")
    act_list = []
    act = []
    title = []
    for item in activities_list:
        if item["snippet"].get("title") in title:
            continue
        if item["snippet"].get("type") != "upload":
            continue
        title.append(item["snippet"].get("title"))
        act.append({"title":item["snippet"].get("title")})
        act.append({"description":item.get("snippet").get("description")})
        act.append({"url":item["snippet"]["thumbnails"]["default"]["url"]})
        act.append({"time":item["snippet"].get("publishedAt")})
        act_list.append(act)  
          
    uper_activities['video_list'] = act_list
    
    pprint.pprint(uper_activities)
    title = uper_activities.get("uper")
    _,token = notion_token()
    pageid = "780d7bfd44a64a37bcb21c5f5278053e"
    result = notion_page_additem(token=token,pageid=pageid,title=title,content=uper_activities)