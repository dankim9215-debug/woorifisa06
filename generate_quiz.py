import os
import glob
import json
from google import genai

# [중구] 클라이언트 설정 시 'http_options'를 통해 v1 버전을 명시합니다.
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options={'api_version': 'v1'}
)

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
            
            # 내용이 너무 길면 오류가 날 수 있으니 적절히 자릅니다.
            content_sample = content[:15000]
            
            print(f"🚀 {date_key} 생성 요청 중...")
            
            # 모델 이름은 'gemini-1.5-flash' 그대로 사용합니다.
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"다음 학습 내용을 바탕으로 10문제 복습 퀴즈를 만드세요. 정답은 <details> 태그로 가려주세요: \n\n {content_sample}"
            )
            
            if response and response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 성공!")
            else:
                print(f"❌ {date_key} 응답 없음")
                
        except Exception as e:
            print(f"❌ {date_key} 에러: {str(e)}")

    # 결과 저장 (빈 리스트라도 저장하여 파일 존재 여부를 확인합니다)
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)
    
    print(f"--- [DEBUG] 최종 저장 결과: {list(quiz_db.keys())} ---")

if __name__ == "__main__":
    generate_quizzes()
