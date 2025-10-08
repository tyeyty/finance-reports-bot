import requests

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DB_ID")

def add_to_notion(title, summary, file_url):
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": "Example Title"}}]},
            "Summary": {"rich_text": [{"text": {"content": "Example summary"}}]},
            "Source": {"url": "https://example.com/file.pdf"},
            "Date": {"date": {"start": "2025-10-08"}},
            "Type": {"select": {"name": "Weekly"}}
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
