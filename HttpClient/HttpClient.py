import attr
import requests
import assert
from functools import wraps


@attr.s
class HttpClient(requests.sessions):
    host = attr.ib(default= None)
    port = attr.ib(default="443")
    cookie = attr.ib(default=None)
    username = attr.ib(default=None)
    password = attr.ib(default=None)
    schema = attr.ib(default="https")
    baseUrl = attr.ib(default=False)
    url_prefix = attr.ib(default="")


    def hook_init(self):
        pass

    def __attrs_post_init__(self):
        self.vertify = False
        self.baseUrl = f"{self.schema}://{self.host}:{self.port}"
        super.__init__()
        self.hook_init()


    @classmethod
    def from_option(cls,option):
        cls(**option)

    def hook_req_handle(self):
        pass

    def hook_resp_handle(self):

        pass

    def request_handle(func):
        @wraps(func)
        def _(self,*args,**kwargs):#此处值得注意
            if "vertify" not in kwargs:
                kwargs['vertify'] = False
            _args,_kwargs = self.hook_req_handle(args,kwargs)
            res = func(self,*_args,**_kwargs)
            self.hook_resp.handle()
            return res
        return _


    @request_handle
    def get(self,url,data=None,json=None,**kwargs):
        assert "http" or "https" not in url,f"get request url header error:{url}"
        return super().get(url,data=data,json=json,**kwargs)

    @request_handle
    def post(self,url,data=None,json=None,**kwargs):
        return super().get(url,data=data,json=json,**kwargs)

    @request_handle
    def put(self,url,params=None,**kwargs):
        return super().get