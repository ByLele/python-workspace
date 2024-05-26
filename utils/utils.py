import logging
import time
from jsonpath_ng import parse
from functools import wraps 


logger = logging.getLogger(__file__)
def show_and_raise_exception(fn):
    @wraps(fn)
    def capture_exception(*arg, **kwargs):
        try:
            logger.info(f"function {fn.__name__}starting")
            start_time = time.time()
            return fn(*arg,**kwargs)
        except Exception as e:
            logger.exception(f"function {fn.__name__} have exception! msg:{e}")
            raise
        finally:
            logger.error(f"function {fn.__name__} SpendTime {time.time() - start_time}")

    return capture_exception


def recursion_json(json_dict, key='', new_value=None, count=10000):
    """
        递归修改字典中的某个key的值（该值不支持为列表-字典整个替换）, 支持指定替换个数；默认是10000个（全量）
        _json({"names":[{"title":"nice"},{"title":"大黄蜂"}]}, "title", "我要上天了", count=1)  ==>  {"names":[{"title":"我要上天了"},{"title":"大黄蜂"}]}
    @param json_dict: 需要被修改的字段数据
    @param key: 需要变更的key
    @param new_value: 对应key的新的值
    @param count:  替换个数; 默认是10000个（全量） count = 2 则只替换前两个
    @return  对源数据体编辑，不返回新对象； 建议使用之前自行深复制对象后进行操作
    """
    # 替换次数应该使用全局变量，以避免递归函数入参对局部变量的影响。
    global REPLACE_COUNT
    REPLACE_COUNT = count
    # 递归
    for k, v in json_dict.items():
        if REPLACE_COUNT > 0 and isinstance(v, dict):
            _json(v, key, new_value, REPLACE_COUNT)
        elif REPLACE_COUNT > 0 and isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
            for i in v:
                _json(i, key, new_value, REPLACE_COUNT)
        else:
            if REPLACE_COUNT > 0 and k == key:
                json_dict[k] = new_value
                REPLACE_COUNT -= 1
    else:
        return True
@show_and_raise_exception
def _json(json_dict, key='', new_value=None, count=10000, json_path=None):
    """
        支持修改字典中的某些key的值, 支持指定替换个数；默认是10000个（全量）；
        支持通过jsonpath修改目标节点的值。传入isjsonpath=True  jsonpath="$.title"；
        替换列表-字典等，请使用json的形式来替换。
        支持通过jsonpath修改目标节点的值。传入isjsonpath=True  jsonpath="$.title"
        _json({"names":[{"title":"nice"},{"title":"大黄蜂"}]}, "title", "我要上天了", count=1)  ==>  {"names":[{"title":"我要上天了"},{"title":"大黄蜂"}]}
        _json({"names": [{"title": "nice"}], "title": "大黄蜂"} , new_value="擎天柱", json_path="$.title")   ==> {'names': [{'title': 'nice'}], 'title': '擎天柱'}

    @param json_dict: 需要被修改的json数据
    @param key: 需要变更的key
    @param new_value: 对应key的新的值
    @param count:  替换个数; 默认是10000个（全量） count = 2 则只替换前两个
    @param json_path: 默认为None, 如果传入有值，则调用jsonpath-ng 进行修改对应的值。
    @return  对源数据体编辑，不返回新对象； 建议使用之前自行深复制对象后进行操作
    """
    if json_path:
        parser = parse(json_path)
        # data = parser.find(json_dict)
        parser.update(json_dict, new_value)
        logger.error(f"_json() jsonpath error!")
    else:
        recursion_json(json_dict, key=key, new_value=new_value, count=count)
