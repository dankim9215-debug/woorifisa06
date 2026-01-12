import os
import glob
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    # 1. 현재 파이썬 파일이 있는 위치(./)에서 .md 파일을 모두 찾습니다.
    md_files = glob.glob('*.md') 
    
    quiz_db = {}
    print(f"--- [확인] 현재 위치의 md 파일들: {md_files} ---")

    if not md_files:
        print("❌ 에러: 파이썬 파일 옆에 .md 파일이 하나도 없습니다!")
        return

    for file_path in md_files:
        # 파일 이름에서 날짜 키 추출 (예: 2026.01.09)
        date_key = file_path.replace('.md', '').replace('.MD', '')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # AI에게 퀴즈 생성 요청 (최신 모델 사용)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                prompt = f"""
            당신은 IT 교육 전문가입니다. 아래 학습일지 내용을 분석하여 10개의 복습 퀴즈를 생성하세요.

            [출제 가이드라인]
            1. 난이도: 중급 (단순 암기보다 원리 이해를 묻는 문제 위주)
            2. 구성: 객관식 5개, 단답형 2개, 코딩 주관식 3개
            3. 핵심 키워드: 클래스 상속, 메서드 타입(static/class), 캡슐화 등 어려운 개념을 우선적으로 포함
            4. 출력 형식: 
               - 사용자가 정답을 바로 보지 못하도록 <details><summary>정답 확인하기</summary>...내용...</details> 태그를 사용
               - 코딩 문제의 모범 답안은 반드시 ```python 코드 블록을 사용

            학습일지 내용:
            {content}
            """
            )
            quiz_db[date_key] = response.text
            print(f"✅ {date_key} 퀴즈 생성 성공!")
            
        except Exception as e:
            print(f"❌ {date_key} 처리 중 에러: {e}")

    # 2. 결과 저장 (같은 위치에 quiz_db.json 생성)
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print("🚀 모든 작업이 완료되었습니다!")

if __name__ == "__main__":
    generate_quizzes()
