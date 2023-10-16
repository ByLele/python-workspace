import requests
token = 'secret_fz8hGuVnnQsTbifpRhXx0SCAfNiqSSPBn7IGfZKh0ww'
r = requests.request(
        "GET",
        "https://www.notion.so/c045802ba2404b80869d13d0f53d6aa4",#字符串为页面id
        headers={"Authorization": "Bearer " + token, "Notion-Version": "2021-05-13"},
    )
print(r.text)
import requests
token = '第二步中获取到的token值'
def post(url,title,content):
    requests.request("POST",
    "https://api.notion.com/v1/pages",
    json={
        "parent": {"type": "database_id", "database_id": "9bcf00dc-e55c-4279-9f3b-177dc325aa18"},
        "properties": {
            "来源": {"url": url},
            "标题": {"title": [{"type": "text", "text": {"content": title}}]},
            "描述": {"rich_text": [{"type": "text", "text": {"content": content}}]},
        },
        "children": [
            {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": [{ "type": "text", "text": { "content": content } }]
            }
            }
        ]
    },
    headers={"Authorization": "Bearer " + token, "Notion-Version": "2021-05-13"},
    )
    print(title + '---' +url) 


if __name__ == "__main__":
    post('https://www.xinhuoip.com','薪火IP全国动态pptp 静态IP 单进程单IP 单窗口单IP','工作室客户量大优惠、支持游戏、试玩、短视频等各类项目，客服QQ：1167064')
