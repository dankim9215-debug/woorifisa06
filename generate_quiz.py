import os
import glob
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

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
            print(f"🚀 {date_key} 생성 시도 중...")

            # 최신 SDK는 모델 명칭 인식이 더 유연합니다.
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=f"다음 내용을 바탕으로 복습 퀴즈 10문제를 생성해줘. 정답은 <details> 태그로 가려줘: \n\n {content[:15000]}"
            )
            
            if response and response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 성공!")
        except Exception as e:
            quiz_db[date_key] = f"실패 에러: {str(e)}"

    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_quizzes()
