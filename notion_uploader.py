import os
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
            "Date": {"date": {"start": date}},        # date 형식: "YYYY-MM-DD"
            "Type": {"select": {"name": type_name}}   # 예: "Weekly", "Monthly"
        }
    }

    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        },
        json=data
    )

    print("🔍 Status Code:", response.status_code)
    print("🔍 Response:", response.text)

    return response


# ✅ 테스트 실행
if __name__ == "__main__":
    add_to_notion(
        title="테스트 보고서",
        summary="Notion API 연결 테스트",
        file_url="https://example.com/test.pdf",
        date="2025-10-20",
        type_name="Weekly"
    )
