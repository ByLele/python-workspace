import os
import pickle
import logging 
import pprint
import json
import yaml
import sys
import time

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import (
    TypeVar
)
from pprint import pprint
import urllib.parse as p
#sys.path.append("/Users/vbnvc/GitRepo/python-workspace")

from utils.utils import show_and_raise_exception
from utils.yaml_deal import YamlDealer 
logger = logging.getLogger(__file__)

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
token = 'secret_fz8hGuVnnQsTbifpRhXx0SCAfNiqSSPBn7IGfZKh0ww'
databaseID = "90cc1a489ec14a78ae14a8de4abcabb7"
headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }
U = TypeVar("U")

class youtube(object):
    """_summary_
    youtube is request api client get subscribe author and get request data
    Args:
        object (_type_): _description_
    """
    def __init__(self,secrets:str,token:str):
        self.yt_client = self.youtube_authenticate(client_secrets_file=secrets,TOKEN=token) 
        self.YDealer = YamlDealer()
    def youtube_authenticate(self,
                             client_secrets_file:str,
                             TOKEN:str)-> U:
        """_summary_
        create a youtube api client 
        Returns:
            U: _description_
        """
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        #client_secrets_file = "./client_secret_847585282559-2v2nh29jlgrhghibmma96suoleqfkek8.apps.googleusercontent.com.json"
        client_secrets_file = client_secrets_file
        creds = None
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        
        #if os.path.exists("token5.pickle"):
        if os.path.exists(TOKEN):
            with open(TOKEN, "rb") as token:
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
    
    def get_video_details(self,youtube:U, **kwargs)-> U:
        return youtube.videos().list(
            part="snippet,contentDetails,statistics",
            **kwargs
        ).execute()
        
    def get_sub(self,youtube:U, **kwargs)-> U:
        return youtube.subscriptions().list(
            part="snippet",
            #mySubscribers=True,
            mine=True,
            maxResults=50,
            **kwargs
        ).execute()
    @show_and_raise_exception
    def activity_channel_list(self,youtube,channelId:str,**kwargs):
        return youtube.activities().list(
            part="snippet",
            channelId=channelId,
            **kwargs
        ).execute()   
    
    def sub_sync(self,youtube):
        """_summary_

        Args:
            youtube (_type_): _description_
        """
        channellist = self.get_sub(youtube)
        items = channellist.get("items")
        #uper_yaml_write(items)
        self.YDealer.YamlWriter(uper_data=items)
        logger.info("uper folder sync sub data ")
        while channellist.get("nextPageToken"):

            channellist = self.get_sub(youtube,pageToken=channellist.get("nextPageToken"))
            items = channellist.get("items")
            self.YDealer.YamlWriter(uper_data=items)
            
        logger.info("sync_sub write yaml success")
        
    @show_and_raise_exception
    def uper_activities(self,youtube,channelId:str)-> dict:

        res = self.activity_channel_list(youtube=youtube,channelId=channelId)

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
