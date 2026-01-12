import os
import glob
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    # 1. 하위 모든 폴더에서 .md 파일을 찾도록 경로 확장
    md_files = glob.glob('**/*.md', recursive=True)
    
    print(f"발견된 마크다운 파일 목록: {md_files}") # 어떤 파일을 찾았는지 로그에 찍힘
    
    quiz_db = {}

    if not md_files:
        print("❌ 마크다운 파일을 하나도 찾지 못했습니다. 폴더 구조를 확인하세요.")
        return

    for file_path in md_files:
        # 파일명만 추출하여 날짜 키 생성
        date_key = os.path.basename(file_path).replace('.md', '').replace('.MD', '')
        
        print(f"Processing: {date_key} (Path: {file_path})")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content.strip()) < 10: continue # 빈 파일은 건너뜀

            try:
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
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                quiz_db[date_key] = response.text
            except Exception as e:
                print(f"오류 ({date_key}): {e}")

    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print(f"✅ 업데이트 완료! 생성된 퀴즈 개수: {len(quiz_db)}")

if __name__ == "__main__":
    generate_quizzes()
