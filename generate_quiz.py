import os
import glob
import json
from google import genai # 최신 라이브러리 사용 권장

# 1. API 설정
# 최신 라이브러리 방식에 맞춰 클라이언트를 초기화합니다.
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    md_files = glob.glob('./*.md')
    quiz_db = {}

    for file_path in md_files:
        date_key = os.path.basename(file_path).replace('.md', '')
        print(f"[{date_key}] 퀴즈 생성 중...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 2. 보강된 프롬프트 설계
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
            
            try:
                # 3. 모델명을 gemini-1.5-flash로 변경하여 404 에러 해결
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                quiz_db[date_key] = response.text
            except Exception as e:
                print(f"오류 발생 ({date_key}): {e}")

    # JSON 데이터베이스 저장
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print("✅ 퀴즈 데이터베이스 업데이트 완료!")

if __name__ == "__main__":
    generate_quizzes()
