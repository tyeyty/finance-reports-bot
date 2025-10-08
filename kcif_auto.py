import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# KCIF 기본 URL
BASE_URL = "https://www.kcif.or.kr"
MONTHLY_URL = "https://www.kcif.or.kr/annual/monthlyList"  # 월간보고서
WEEKLY_URL = "https://www.kcif.or.kr/annual/weeklyList"    # 주간보고서

# 저장 폴더 설정
SAVE_DIR = "./downloads"
os.makedirs(SAVE_DIR, exist_ok=True)

def get_pdf_links(target_url):
    """KCIF 보고서 페이지에서 PDF 링크들을 가져오기"""
    response = requests.get(target_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    pdf_links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.endswith(".pdf"):
            full_url = href if href.startswith("http") else f"{BASE_URL}{href}"
            pdf_links.append(full_url)
    return pdf_links

def download_pdfs(links):
    """PDF 파일을 다운로드"""
    for link in links:
        file_name = link.split("/")[-1]
        file_path = os.path.join(SAVE_DIR, file_name)
        if os.path.exists(file_path):
            print(f"✅ 이미 존재: {file_name}")
            continue
        print(f"⬇️ 다운로드 중: {file_name}")
        pdf_data = requests.get(link).content
        with open(file_path, "wb") as f:
            f.write(pdf_data)
        print(f"📁 저장 완료: {file_path}")

def main():
    today = datetime.today()
    weekday = today.weekday()  # 0=월요일, 6=일요일

    # 월간/주간 URL 결정
    if today.day == 1:
        target_url = MONTHLY_URL
        print("📅 오늘은 1일, 월간 보고서 다운로드")
    elif weekday == 0:  # 월요일
        target_url = WEEKLY_URL
        print("📅 오늘은 월요일, 주간 보고서 다운로드")
    else:
        print("❌ 오늘은 보고서를 다운로드할 날이 아닙니다.")
        return

    print("🔍 KCIF 보고서 링크 탐색 중...")
    pdf_links = get_pdf_links(target_url)
    if not pdf_links:
        print("❌ PDF 링크를 찾지 못했습니다.")
        return
    print(f"📄 총 {len(pdf_links)}개 파일 발견")
    download_pdfs(pdf_links)
    print("🎉 모든 다운로드 완료!")

if __name__ == "__main__":
    main()
