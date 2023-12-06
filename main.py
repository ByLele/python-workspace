
from pprint import pprint


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
    #test_playlist()
    
    from collections import Counter

    def remove_duplicates(data):
        if not isinstance(data, dict) or 'video_list' not in data:
            raise ValueError("Invalid input format. Expected a dictionary with 'video_list' key.")

        for sublist in data['video_list']:
            if not isinstance(sublist, list):
                raise ValueError("Invalid video_list format. Expected a list of dictionaries.")

        all_titles = [item['title'] for sublist in data['video_list'] for item in sublist if isinstance(item, dict) and 'title' in item]
        if not all_titles:
            return data

        title_count = Counter(all_titles)
        threshold = 0.8 * len(data['video_list'])

        filtered_titles = {title: count for title, count in title_count.items() if count >= threshold}
        new_video_list = [[item for item in sublist if not (isinstance(item, dict) and 'title' in item and item['title'] in filtered_titles)] for sublist in data['video_list']]
        data['video_list'] = new_video_list

        return data

    # 示例用法
    input_data = {'uper': '观察者网',
                'video_list': [
                    [{'title': '向松祚：粤港澳大湾区和全球其他几个大湾区相比，最大的不足是缺少原创性科学创新'}, 
                    {'description': ''}, 
                    {'url': 'https://i.ytimg.com/vi/cuUcHL57S5w/default.jpg'}, 
                    {'publishedAt': '2023-12-06T07:10:02+00:00'}, 
                    {'title': '向松祚：硅谷的科技创新领先全球是因为人才，这方面我很赞赏华为'}, 
                    {'description': ''}, 
                    {'url': 'https://i.ytimg.com/vi/1oISacYdI4w/default.jpg'}, 
                    {'publishedAt': '2023-12-06T06:33:07+00:00'}, 
                    {'title': '奥地利前总理：联合国等国际机构虚弱又无效，不然俄乌冲突早结束了'}, 
                    {'description': ''}, 
                    {'url': 'https://i.ytimg.com/vi/6BwJUMtQYUg/default.jpg'}, 
                    {'publishedAt': '2023-12-06T06:19:49+00:00'}, 
                    {'title': '瑞典前首相：世界银行行长一直是美国人，IMF总裁一直是欧洲人，我们还问为何发展中国家不信任我们'}, 
                    {'description': ''}, 
                    {'url': 'https://i.ytimg.com/vi/KZleVYAc8cI/default.jpg'}, 
                    {'publishedAt': '2023-12-06T02:29:44+00:00'}, 
                    {'title': '吓人！重庆一摩托车弯道侧翻，2人被卷入大车车底'}, 
                    {'description': ''}, 
                    {'url': 'https://i.ytimg.com/vi/wqzB8Qz9ym0/default.jpg'}, 
                    {'publishedAt': '2023-12-05T11:30:31+00:00'}]
                ]
                }

    try:
        result = remove_duplicates(input_data)
        pprint(result)
    except ValueError as e:
        print(e)
