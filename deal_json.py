import json
from logger import logger
from pprint import pprint
def convert_json()->None:
    with open("./2.json", "r",errors='ignore',encoding='utf8') as f:
        # txt = str(f.read()).replace('\'','"').replace("\"S","\'")
        txt = str(f.read()).replace('\'', '"')
        pprint(txt)
        aa=json.loads(txt)
        print(1)
        return json.loads(txt)

class dealer(object):
    def __init__(self) -> None:
        pass
    
    def Reader(self) -> None:
        with open("./2.json",'r',encoding='utf-8') as file:
            req_data = file.read()
            json_data = json.loads(req_data)
            logger.info(json_data)
            print(type(json_data))
        
        
if __name__ == "__main__":
    
    logger.info(12341241324)
    # D = dealer()
    # D.Reader()
    convert_json()