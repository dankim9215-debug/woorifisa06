import os
import glob
import json
from google import genai

# 다시 v1beta로 시도 (v1에서 404가 났으므로)
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options={'api_version': 'v1beta'}
)

def generate_quizzes():
    # [디버깅] 사용 가능한 모델 리스트 출력
    print("--- [DEBUG] 사용 가능한 모델 목록 확인 중... ---")
    try:
        for m in client.models.list():
            print(f"발견된 모델: {m.name}")
    except Exception as e:
        print(f"모델 리스트 확인 실패: {e}")

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
            
            # 가장 표준적인 이름으로 재시도
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=f"다음 학습 내용을 바탕으로 10문제 복습 퀴즈를 만드세요: \n\n {content[:10000]}"
            )
            
            if response and response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 생성 성공!")
            
        except Exception as e:
            quiz_db[date_key] = f"실패 에러: {str(e)}"
            print(f"❌ {date_key} 최종 실패: {e}")

    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_quizzes()
