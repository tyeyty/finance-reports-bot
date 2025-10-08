import requests

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DB_ID")

def add_to_notion(title, summary, file_url, date, type_name):
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "Summary": {"rich_text": [{"text": {"content": summary}}]},
            "Source": {"url": file_url},
            "Date": {"date": {"start": date}},        # 여기서 date는 "YYYY-MM-DD"
            "Type": {"select": {"name": type_name}}  
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
