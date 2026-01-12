import os
import glob
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    # 1. 모든 가능성을 열어두고 파일 검색
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    
    print(f"--- [DEBUG] 발견된 파일 목록: {md_files} ---")
    
    quiz_db = {}

    for file_path in md_files:
        # 2. 파일 이름 분석 로그
        file_name = os.path.basename(file_path)
        date_key = file_name.replace('.md', '').replace('.MD', '')
        print(f"--- [DEBUG] 현재 처리 중인 파일: {file_name} (Key: {date_key}) ---")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"--- [DEBUG] 파일 내용 길이: {len(content)} 자 ---")
            
            if len(content.strip()) < 10:
                print(f"⚠️ {file_name} 내용이 너무 짧아 스킵합니다.")
                continue

            # 3. AI 요청 및 응답 확인
            print(f"🚀 Gemini AI에게 {date_key} 퀴즈 생성 요청 중...")
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"학습 내용을 바탕으로 10문제 복습 퀴즈를 만드세요: {content}"
            )
            
            if response and response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 생성 성공! (데이터 크기: {len(response.text)})")
            else:
                print(f"❌ {date_key} AI 응답이 비어있습니다.")

        except Exception as e:
            print(f"❌ {date_key} 에러 발생: {str(e)}")

    # 4. 최종 저장 전 상태 확인
    print(f"--- [DEBUG] 최종 JSON에 담긴 날짜들: {list(quiz_db.keys())} ---")
    
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    print("🚀 모든 과정 종료 및 파일 저장 완료")

if __name__ == "__main__":
    generate_quizzes()
