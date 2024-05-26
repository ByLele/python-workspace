import os
import time
import logging

#from notion import notion_sync
from config.config import setting
from youtube import youtube
from utils.yaml_deal import YamlDealer
from utils.utils import show_and_raise_exception
from pprint import pprint

logging.basicConfig(
        level=logging.INFO,
        format="{asctime} {levelname:>8} {process} [{threadName:>12}] {name} ({filename}:{lineno}): {message}",
        style="{",
    )
       
       
logger= logging.getLogger(__file__)

@show_and_raise_exception
def main(
    
)->None:
    logger.info("========================create youtube client================")
    YClient = youtube(secrets=setting.CLIENT_SECRETS_FILE,token=setting.TOKEN)
    YClient.sub_sync(youtube=YClient.yt_client)
    
    
    YDealer = YamlDealer()
    if not os.path.exists("./uper/"):
        logger.error("./uper not exists no subscirber need reader")
    uper_data = YDealer.YamlReader("./uper")
    
    if not uper_data:
        logger.error(f"not subscribeser to reader msg:{uper_data}")
    
    for item in uper_data:
        try:
            uper_act = YClient.uper_activities(youtube=YClient.yt_client,channelId=item)       
            time.sleep(3)      
            pprint(uper_act)    
            #notion_sync(uper=uper_act,databaseID=a,headers=h)
        except Exception as e:
            logger.error(f"subscriber update by ./uper data failed,msg{e}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="{asctime} {levelname:>8} {process} [{threadName:>12}] {name} ({filename}:{lineno}): {message}",
        style="{",
    )
       
       
    logger = logging.getLogger(__file__)
    main()
    