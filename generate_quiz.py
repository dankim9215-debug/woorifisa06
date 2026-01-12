import os
import glob
import json
from google import genai

# 1. 클라이언트 설정 (버전 명시)
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options={'api_version': 'v1'}
)

def generate_quizzes():
    # 모든 .md 파일 검색
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    print(f"--- [DEBUG] 발견된 파일 목록: {md_files} ---")
    
    quiz_db = {}

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_key = file_name.lower().replace('.md', '').strip()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 50: continue

            print(f"🚀 {date_key} 퀴즈 생성 중...")
            
            # [수정] 모델명을 'gemini-1.5-flash'로 고정해서 호출
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=f"다음 학습 내용을 바탕으로 복습 퀴즈 10문제를 생성해줘. 정답은 <details> 태그로 가려줘: \n\n {content[:15000]}"
            )
            
            if response and response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 생성 성공!")
            else:
                print(f"❌ {date_key} 응답 텍스트가 없음")
            
        except Exception as e:
            # 404 에러가 나면 모델명을 다르게 해서 한 번 더 시도
            print(f"⚠️ {date_key} 1차 시도 실패, 재시도 중... 에러: {e}")
            try:
                response = client.models.generate_content(
                    model='models/gemini-1.5-flash',
                    contents=f"다음 내용을 바탕으로 퀴즈 10문제를 만드세요: {content[:10000]}"
                )
                if response.text:
                    quiz_db[date_key] = response.text
                    print(f"✅ {date_key} 재시도 성공!")
            except Exception as e2:
                print(f"❌ {date_key} 최종 실패: {e2}")

    # 결과 저장
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print(f"--- [DEBUG] 최종 저장 결과: {list(quiz_db.keys())} ---")

if __name__ == "__main__":
    generate_quizzes()
