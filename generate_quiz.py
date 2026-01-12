import os
import glob
import json
import google.generativeai as genai

# 1. API 설정
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    # 현재 폴더의 모든 .md 파일 검색
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    print(f"--- [DEBUG] 발견된 파일: {md_files} ---")
    
    quiz_db = {}
    
    # 2. 모델 설정 (경로를 명시적으로 작성하여 404 에러 방지)
    model = genai.GenerativeModel('models/gemini-1.5-flash')

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        # 웹에서 입력할 날짜 키 (소문자 변환, 확장자 제거, 공백 제거)
        date_key = file_name.lower().replace('.md', '').strip()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 50: continue

            print(f"🚀 {date_key} 퀴즈 생성 요청 중...")
            
            # 3. AI 문제 생성
            response = model.generate_content(
                f"다음 학습 내용을 바탕으로 복습 퀴즈 10문제를 생성해줘. 정답은 <details> 태그로 가려줘: \n\n {content[:15000]}"
            )
            
            if response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 생성 성공!")
            
        except Exception as e:
            print(f"❌ {date_key} 에러 발생: {str(e)}")

    # 4. 결과 저장
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print(f"--- [DEBUG] 최종 저장 완료: {list(quiz_db.keys())} ---")

if __name__ == "__main__":
    generate_quizzes()
