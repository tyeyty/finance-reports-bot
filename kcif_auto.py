import os
import requests
from bs4 import BeautifulSoup
import pdfplumber
from openai import OpenAI
from datetime import datetime

# 환경 변수
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DB_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# KCIF URLs
BASE_URL = "https://www.kcif.or.kr"
MONTHLY_URL = "https://www.kcif.or.kr/annual/monthlyList"
WEEKLY_URL = "https://www.kcif.or.kr/annual/weeklyList"

SAVE_DIR = "./downloads"
os.makedirs(SAVE_DIR, exist_ok=True)

def get_target_pdfs(target_url, type_name):
    response = requests.get(target_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    pdf_links = []

    if type_name == "Weekly":
        target_titles = ["주간 Wall Street 인사이트", "주간 이슈"]
    else:  # Monthly
        target_titles = ["월간 보고서"]

    for a_tag in soup.find_all("a", href=True):
        text = a_tag.get_text(strip=True)
        href = a_tag["href"]
        # view.jsp + ftype=pdf 있는 링크만 PDF로 판단
        if any(title in text for title in target_titles) and "view.jsp" in href and "ftype=pdf" in href:
            full_url = href if href.startswith("http") else f"{BASE_URL}{href}"
            pdf_links.append((text, full_url))
    
    return pdf_links

def download_pdf(link):
    # FileName 쿼리에서 이름 추출
    if "FileName=" in link:
        file_name = link.split("FileName=")[-1]
        file_name = requests.utils.unquote(file_name)
    else:
        file_name = link.split("/")[-1]

    file_path = os.path.join(SAVE_DIR, file_name)
    if os.path.exists(file_path):
        print(f"✅ 이미 존재: {file_name}")
        return file_path

    print(f"⬇️ 다운로드 중: {file_name}")
    pdf_data = requests.get(link).content
    with open(file_path, "wb") as f:
        f.write(pdf_data)
    print(f"📁 저장 완료: {file_path}")
    return file_path

def summarize_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    prompt = f"다음 보고서를 중학생이 이해가능한 수준으로 요약해줘:\n{text[:6000]}"
    summary = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )
    return summary.choices[0].message.content

def add_to_notion(title, summary, file_url, date, type_name):
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "Summary": {"rich_text": [{"text": {"content": summary}}]},
            "Source": {"url": file_url},
            "Date": {"date": {"start": date}},
            "Type": {"select": {"name": type_name}}
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
    if response.status_code in [200, 201]:
        print(f"✅ Notion 업로드 완료: {title}")
    else:
        print(f"❌ Notion 업로드 실패: {response.text}")

def main():
    today = datetime.today()
    weekday = today.weekday()

    if today.day == 1:
        target_url = MONTHLY_URL
        type_name = "Monthly"
        print("📅 오늘은 1일, 월간 보고서 다운로드")
    elif weekday == 0:
        target_url = WEEKLY_URL
        type_name = "Weekly"
        print("📅 오늘은 월요일, 주간 보고서 다운로드")
    else:
        print("❌ 오늘은 보고서를 다운로드할 날이 아닙니다.")
        return

    pdf_links = get_target_pdfs(target_url, type_name)
    if not pdf_links:
        print("❌ PDF 링크를 찾지 못했습니다.")
        return

    for title, link in pdf_links:
        file_path = download_pdf(link)
        summary = summarize_pdf(file_path)
        add_to_notion(
            title=title,
            summary=summary,
            file_url=link,
            date=today.strftime("%Y-%m-%d"),
            type_name=type_name
        )

if __name__ == "__main__":
    main()
