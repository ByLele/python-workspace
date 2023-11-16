NOTION_TOKEN = "secret_fz8hGuVnnQsTbifpRhXx0SCAfNiqSSPBn7IGfZKh0ww"
DATABASE_ID = "780d7bfd44a64a37bcb21c5f5278053e"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

import requests
import datetime
from pprint import pprint
def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results



if __name__ == "__main__":
    pages = get_pages()
    pprint(pages)
    for page in pages:
        page_id = page["id"]
        props = page["properties"]
    
        title = props["Title"]["rich_text"][0]["text"]["content"]
        published = props["Published"]["date"]["start"]
        published = datetime.fromisoformat(published)