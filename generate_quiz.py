import google.generativeai as genai
import os
import glob
import json
from datetime import datetime

# 1. Gemini API 설정
# GitHub Secrets에 등록한 GEMINI_API_KEY를 환경변수로 가져옵니다.
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def generate_10_quizzes(content):
    """
    학습 내용을 바탕으로 10개의 심화 문제를 생성하는 함수입니다.
    """
    prompt = f"""
    당신은 실무 중심의 컴퓨터 교육 전문가입니다. 아래 학습 내용을 바탕으로 10개의 복습 퀴즈를 만드세요.
    
    [문제 구성]
    - 객관식 5문제: 핵심 이론 (상속, 메서드 타입, 메모리 구조 등)
    - 단답형 2문제: 주요 키워드 및 내장 함수
    - **코딩 주관식 3문제**: 직접 코드를 작성해야 하는 실습형 문제 (모범 답안 포함)
    
    [가이드라인]
    - 모든 문제는 마크다운(Markdown) 형식을 사용할 것.
    - 정답과 상세 해설은 반드시 <details><summary>정답 확인하기</summary>...내용...</details> 태그로 감싸서 숨길 것.
    - 코드 블록은 반드시 ```python 문법을 사용할 것.
    
    학습 내용:
    {content}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"문제 생성 중 오류 발생: {str(e)}"

def run_automation():
    # 2. 모든 마크다운 파일 탐색 (학습한 glob 모듈 활용)
    # 파일명 예시: 2026.01.08.md
    md_files = glob.glob('./*.md')
    quiz_database = {}

    for file_path in md_files:
        # 파일명에서 날짜 키 추출 (예: 2026.01.08)
        date_key = os.path.basename(file_path).replace('.md', '')
        
        print(f"[{date_key}] 날짜의 퀴즈 생성 중...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
            # 10개 문제 생성 실행
            quiz_database[date_key] = generate_10_quizzes(log_content)

    # 3. 생성된 퀴즈 뭉치를 JSON 데이터베이스로 저장
    # 이 파일은 웹(index.html)에서 불러와서 사용하게 됩니다.
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_database, f, ensure_ascii=False, indent=4)
    
    print("✅ 모든 날짜의 퀴즈 데이터베이스 업데이트 완료!")

if __name__ == "__main__":
    run_automation()
