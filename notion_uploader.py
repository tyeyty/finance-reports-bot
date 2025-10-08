import requests

NOTION_TOKEN = "YOUR_NOTION_API_KEY"
DATABASE_ID = "YOUR_DATABASE_ID"

def add_to_notion(title, summary, file_url):
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "Summary": {"rich_text": [{"text": {"content": summary}}]},
            "Source": {"url": file_url}
        }
    }
    requests.post(
        "https://api.notion.com/v1/pages",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        },
        json=data
    )
