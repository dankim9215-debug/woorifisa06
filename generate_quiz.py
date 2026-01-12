import os
import glob
import json
from google import genai

# 1. API 클라이언트 설정
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    # 모든 위치의 md 파일을 찾습니다.
    md_files = glob.glob('**/*.md', recursive=True)
    print(f"--- [DEBUG] 발견된 파일: {md_files} ---")
    
    quiz_db = {}

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_key = file_name.replace('.md', '').replace('.MD', '')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 50: continue

            print(f"🚀 {date_key} 퀴즈 생성 중...")
            
            # 모델명을 최신 표준형으로 설정
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"다음 IT 학습 내용을 바탕으로 복습 퀴즈 10문제를 생성해줘. 정답은 <details> 태그로 가려줘: \n\n {content}"
            )
            
            if response and response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 생성 성공!")
            
        except Exception as e:
            print(f"❌ {date_key} 에러 발생: {str(e)}")

    # 결과 저장 (이 파일이 생성되어야 웹에서 읽음)
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print(f"--- [DEBUG] 최종 저장된 날짜들: {list(quiz_db.keys())} ---")

if __name__ == "__main__":
    generate_quizzes()
