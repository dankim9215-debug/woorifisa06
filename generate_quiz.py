import os
import glob
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_quizzes():
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    print(f"--- [DEBUG] 발견된 파일: {md_files} ---")
    
    quiz_db = {}

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        # 날짜 키를 정확하게 추출 (예: 2026.01.09)
        date_key = file_name.lower().replace('.md', '').strip()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 파일 내용이 너무 길면 AI가 거부할 수 있으므로 앞부분 10,000자만 자름
            content_sample = content[:10000]
            
            print(f"🚀 {date_key} 생성 시작...")
            
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"다음 학습 내용을 요약해서 10문제 퀴즈를 만들어줘. 정답은 <details> 태그로 가려줘: \n\n {content_sample}"
            )
            
            if response and response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 성공!")
            else:
                print(f"❌ {date_key} AI 응답 텍스트 없음")
                
        except Exception as e:
            print(f"❌ {date_key} 에러: {str(e)}")

    # [수정] 데이터가 없더라도 빈 상태를 확인하기 위해 무조건 저장
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    
    print(f"--- [DEBUG] 최종 저장 결과: {list(quiz_db.keys())} ---")

if __name__ == "__main__":
    generate_quizzes()
