import json
from pprint import  pprint

uper_data_obj = {'+1': {'type': 'people',
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

def uper_content_load(filepath="uperDatabase.json"):
    with open(filepath) as f:

        data =  f.read()
        json_obj = json.loads(data)
    return json_obj

if __name__ == "__main__":

    data = uper_content_load("uperDatabase.json")
    print(type(data))
    pprint(data)