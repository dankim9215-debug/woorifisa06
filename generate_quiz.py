import os
import glob
import json
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. API 설정 및 'v1' 정식 버전 강제 지정
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    print(f"--- [DEBUG] 발견된 파일: {md_files} ---")
    
    quiz_db = {}
    
    # 2. 모델 설정
    model = genai.GenerativeModel('gemini-1.5-flash')

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_key = file_name.lower().replace('.md', '').strip()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 50: continue

            print(f"🚀 {date_key} 퀴즈 생성 요청 중...")
            
            # [수정] request_options를 통해 v1 API를 사용하도록 강제함
            response = model.generate_content(
                f"다음 학습 내용을 바탕으로 복습 퀴즈 10문제를 생성해줘. 정답은 <details> 태그로 가려줘: \n\n {content[:15000]}",
                request_options=RequestOptions(api_version='v1')
            )
            
            if response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 생성 성공!")
            
        except Exception as e:
            print(f"❌ {date_key} 에러 발생: {str(e)}")

    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print(f"--- [DEBUG] 최종 저장 결과: {list(quiz_db.keys())} ---")

if __name__ == "__main__":
    generate_quizzes()
