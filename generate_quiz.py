import os
import glob
import json
import google.generativeai as genai

# API 설정
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    print(f"--- [DEBUG] 발견된 파일: {md_files} ---")
    
    quiz_db = {}

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_key = file_name.lower().replace('.md', '').strip()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 50: continue

            print(f"🚀 {date_key} 생성 시도 중...")
            
            # [수정] 가장 호환성이 높은 모델 명칭 시도
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"10문제 퀴즈 만들어줘: {content[:10000]}")
            except:
                # 위 방식 실패 시 대체 모델 명칭 사용
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                response = model.generate_content(f"10문제 퀴즈 만들어줘: {content[:10000]}")
            
            if response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 성공!")
            
        except Exception as e:
            print(f"❌ {date_key} 에러: {str(e)}")
            # 에러 발생 시 웹에서 확인할 수 있도록 메시지 저장
            quiz_db[date_key] = f"퀴즈 생성 실패: {str(e)}"

    # 최종 저장
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print(f"--- [DEBUG] 저장 완료: {list(quiz_db.keys())} ---")

if __name__ == "__main__":
    generate_quizzes()
