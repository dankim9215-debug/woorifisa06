import os
import glob
import json
import google.generativeai as genai # 안정적인 구형 라이브러리 사용

# API 설정
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    # 현재 폴더의 모든 .md 파일 검색
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    print(f"--- [DEBUG] 발견된 파일: {md_files} ---")
    
    quiz_db = {}
    # 모델 초기화 (가장 안정적인 1.5-flash)
    model = genai.GenerativeModel('gemini-1.5-flash')

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_key = file_name.lower().replace('.md', '').strip()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 50: continue

            print(f"🚀 {date_key} 생성 요청 중...")
            
            # 퀴즈 생성 요청
            response = model.generate_content(
                f"다음 학습 내용을 바탕으로 복습 퀴즈 10문제를 생성해줘. 정답은 <details> 태그로 가려줘: \n\n {content[:15000]}"
            )
            
            if response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 성공!")
            
        except Exception as e:
            print(f"❌ {date_key} 에러: {str(e)}")

    # 결과 저장
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print(f"--- [DEBUG] 최종 저장 결과: {list(quiz_db.keys())} ---")

if __name__ == "__main__":
    generate_quizzes()
