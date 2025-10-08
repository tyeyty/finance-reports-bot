import pdfplumber
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

def summarize_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)
    prompt = f"다음 보고서를 중학생이 이해가능한 수준으로 요약해줘:\n{text[:6000]}"
    summary = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )
    return summary.choices[0].message.content
