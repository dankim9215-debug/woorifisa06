import os
import glob
import json
from google import genai

# API 클라이언트 설정
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    # 모든 .md 파일을 찾습니다.
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    print(f"--- [DEBUG] 발견된 파일: {md_files} ---")
    
    quiz_db = {}

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_key = file_name.replace('.md', '').replace('.MD', '')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 20: continue

            print(f"🚀 {date_key} 퀴즈 생성 요청 중...")
            
            # [수정포인트] 모델명 앞에 'models/'를 명시적으로 붙여줍니다.
            response = client.models.generate_content(
                model="models/gemini-1.5-flash", 
                contents=f"다음 내용을 바탕으로 10문제 복습 퀴즈를 만드세요: {content}"
            )
            
            if response and response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 생성 성공!")
            
        except Exception as e:
            print(f"❌ {date_key} 에러: {e}")

    # 결과 저장
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print(f"--- [DEBUG] 저장된 날짜들: {list(quiz_db.keys())} ---")

if __name__ == "__main__":
    generate_quizzes()
