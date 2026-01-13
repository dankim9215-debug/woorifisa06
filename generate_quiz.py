import os
import glob
import json
import time # [추가] 시간 지연을 위해 필요합니다.
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options={'api_version': 'v1beta'}
)

def generate_quizzes():
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    quiz_db = {}

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_key = file_name.lower().replace('.md', '').strip()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 50: continue
            
            # [핵심] 429 에러 방지를 위해 요청 전 6초간 휴식
            print(f"💤 {date_key} 생성 전 잠시 대기 중 (6초)...")
            time.sleep(6) 
            
            print(f"🚀 {date_key} 생성 시도 중 (사용 모델: gemini-2.0-flash)...")
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"다음 학습 내용을 바탕으로 복습 퀴즈 10문제를 생성해줘. 정답은 <details> 태그로 가려줘: \n\n {content[:10000]}"
            )
            
            if response and response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 생성 성공!")
            
        except Exception as e:
            # 할당량 초과 시 1분 대기 후 재시도할 수도 있지만, 우선 로그를 남깁니다.
            quiz_db[date_key] = f"실패 에러: {str(e)}"
            print(f"❌ {date_key} 실패: {e}")

    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_quizzes()
