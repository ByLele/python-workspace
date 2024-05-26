import yaml
import logging
import os


logger = logging.getLogger(__file__)

from utils.utils import show_and_raise_exception
from typing import(
    NamedTuple,
    AnyStr,
    TypeVar
)

_T = TypeVar("_T")
class UperData(NamedTuple):
    author: str
    kind: str
    etag: str
    snippet: str
    
class YamlDealer(object):
    def __init__(self) -> None:
        pass 
    @show_and_raise_exception
    def YamlWriter(self,uper_data) -> None:
    

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
            if os.path.exists(filename):
                continue
            
            with open(filename,"w+",encoding='utf-8') as f:
                yaml.dump(uper_data,f,allow_unicode=True)
            

    def YamlReader(self,filepath: str) -> list:
        channelId = []
        for root, dirs, files in os.walk(filepath):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, "r",encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                    #print(yaml_data)
                    if 'snippet' in yaml_data and 'channelId' in yaml_data['snippet']['resourceId']:
                        channel_id = yaml_data['snippet']['resourceId']['channelId']
                        channelId.append(channel_id)
                        
        logger.info("channelId read success")
        return channelId
    