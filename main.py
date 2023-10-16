from pyyoutube import Client,Api
import pprint


api_token = "AIzaSyDoEYdqLiSNXKG-y6hELA0_daS7YrRHstY"
def test_client():
    
    print(123)
    client = Client(api_key=api_token)
    print(client)
    resp = client.channels.list(
        parts=["id", "snippet"],
        channel_id="UCa-vrCLQHviTOVnEKDOdetQ"    
    )
    resp = resp.items[0].to_dict()
    #pprint.pprint(resp)

def test_api():
    api = Api(api_key=api_token)
    r = api.get_subscription_by_me(
        mine=True,
        parts=["id","snippet"],
        count=2
    )
    print(r.items)
    for item in r.items:
        pprint.pprint(item.to_dict())
    #pprint.pprint(r.items[0].to_dict())
    
    
def test_playlist():
    api = Api(api_key=api_token)
    r = api.get_playlist_by_id(playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw")
    pprint.pprint(r.items)
    
if __name__=="__main__":
    pass
    #test_api()
    test_playlist()