import os
import glob
import json
from google import genai

# v1 정식 버전 사용
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options={'api_version': 'v1'}
)

def generate_quizzes():
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    quiz_db = {}

    # 시도해볼 모델 후보군 리스트
    model_candidates = [
        'gemini-1.5-flash',
        'models/gemini-1.5-flash',
        'gemini-1.5-pro',
        'models/gemini-1.5-pro'
    ]

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_key = file_name.lower().replace('.md', '').strip()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 50: continue
            
            success = False
            for model_name in model_candidates:
                try:
                    print(f"🚀 {date_key} 생성 시도 중 (모델: {model_name})...")
                    response = client.models.generate_content(
                        model=model_name,
                        contents=f"다음 내용을 바탕으로 10문제 복습 퀴즈를 생성해줘. 정답은 <details> 태그로 가려줘: \n\n {content[:10000]}"
                    )
                    if response and response.text:
                        quiz_db[date_key] = response.text
                        print(f"✅ {date_key} 생성 성공! (사용한 모델: {model_name})")
                        success = True
                        break # 성공하면 다음 파일로
                except Exception as model_err:
                    print(f"⚠️ {model_name} 실패: {model_err}")
                    continue
            
            if not success:
                quiz_db[date_key] = "모든 모델 후보군이 404 에러로 실패했습니다. API 키의 모델 권한을 확인하세요."

        except Exception as e:
            quiz_db[date_key] = f"파일 읽기/처리 에러: {str(e)}"

    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_quizzes()
