import requests
from bs4 import BeautifulSoup
import re

def search_namuwiki(keyword):
    search_url = f"https://namu.wiki/w/{keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(search_url, headers=headers)

    if res.status_code != 200:
        print("❌ 문서를 찾을 수 없습니다.")
        return

    soup = BeautifulSoup(res.text, 'html.parser')
    content_div = soup.find('div', class_='_1799jGvp')  # 본문이 들어 있는 div

    if not content_div:
        print("❌ 문서 구조를 파악할 수 없습니다.")
        return

    results = {}
    current_section = "개요"
    results[current_section] = ""

    for tag in content_div.find_all(['h2', 'h3', 'p', 'ul']):
        if tag.name in ['h2', 'h3']:
            title = tag.get_text(strip=True)
            # "개요", "연도", "역사", "유래", "특징" 등의 섹션만 추출
            if re.search(r"(개요|연도|역사|유래|특징|종류|기타|구조|원리)", title):
                current_section = title
                results[current_section] = ""
        elif tag.name in ['p', 'ul']:
            if current_section not in results:
                results[current_section] = ""
            results[current_section] += tag.get_text(strip=True) + "\n"

    # 전체 결과 출력
    for section, content in results.items():
        print(f"\n📌 {section}\n{content.strip()}\n{'─'*50}")

# ▶ 실행
search_keyword = input("🔍 나무위키에서 검색할 단어를 입력하세요: ")
search_namuwiki(search_keyword)
