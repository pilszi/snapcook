import requests
from bs4 import BeautifulSoup

# 1. 크롤링할 대상 URL (파라미터 제거한 깔끔한 주소)


# 2. 브라우저인 척 위장하기 위한 Header 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 서버가 보낸 HTML 본문 중 핵심 부분을 터미널에 출력해서 클래스명 확인하기
print(response.text[:2000])  # 앞쪽 2000글자 출력

# try:
#     # 3. 페이지 HTML 가져오기
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, "html.parser")
        
#         # 4. 원하는 데이터 추출하기 (개발자 도구에서 Element를 우클릭해서 selector를 분석해야 합니다)
#         # 예시: 제목 가져오기
#         # (실제 사이트의 태그명이나 클래스명 구조에 맞게 수정해야 합니다)
#         title = soup.select_one("h1") or soup.select_one(".RecipeDetailstyle__Title-q7sykd-4 kIVrZW") # 예시 클래스명
#         # 수정 코드 (디버깅용 print 추가)
#         print("응답 상태 코드:", response.status_code) # 200이 잘 나오는지 확인

#         title = soup.select_one(".recipe-title")
#         if title:
#             print("레시피 제목:", title.text.strip())
#         else:
#             print("제목을 찾지 못했습니다. 태그나 클래스명을 다시 확인하세요.")
            
#         # 예시: 난이도 및 소요시간 가져오기
#         # preview 화면에 보이는 '소요시간 20분', '난이도' 등의 텍스트를 담고 있는 클래스명을 찾습니다.
#         # time_info = soup.select_one(".some-time-class-name")
        
#         # 예시: 재료 리스트 가져오기
#         # ingredients = soup.select(".ingredient-item-class")
#         # for ing in ingredients:
#         #     print(ing.text.strip())

#     else:
#         print(f"접근 실패 (Status Code: {response.status_code})")

# except Exception as e:
#     print("에러 발생:", e)