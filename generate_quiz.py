import os
import glob
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    # [수정] woorifisa06 폴더 안의 모든 .md 파일을 찾습니다.
    # 만약 폴더명이 대소문자를 구분한다면 정확히 맞춰주세요.
    search_path = os.path.join('woorifisa06', '**', '*.md')
    md_files = glob.glob(search_path, recursive=True)
    
    print(f"--- [디버그] 'woorifisa06' 폴더 내 검색 결과 ---")
    print(f"검색 경로: {search_path}")
    print(f"발견된 파일 총 {len(md_files)}개")
    for f in md_files:
        print(f"찾은 파일: {f}")
    print("---------------------------------------")

    quiz_db = {}

    if not md_files:
        print("❌ 에러: 'woorifisa06' 폴더 내에 .md 파일이 없습니다!")
        return

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        # 날짜 키 생성 (확장자 제거)
        date_key = file_name.replace('.md', '').replace('.MD', '')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content.strip()) < 20: continue

        print(f"🚀 {date_key} 퀴즈 생성 중...")
        
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
            print(f"❌ {date_key} 생성 실패: {e}")

    # 최종 결과 저장 (이 파일은 루트에 저장되어 웹에서 읽을 수 있게 합니다)
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print(f"✅ 완료! {len(quiz_db)}개의 데이터 저장됨.")

if __name__ == "__main__":
    generate_quizzes()
