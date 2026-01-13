import os
import glob
import json
import time
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options={'api_version': 'v1beta'}
)

def generate_quizzes():
    md_files = glob.glob('*.md') + glob.glob('*.MD')
    quiz_db = {}

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_key = file_name.lower().replace('.md', '').strip()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 50: continue
            
            # [최적화] 대기 시간을 12초로 늘려 분당 요청 수(RPM)를 안전하게 관리합니다.
            print(f"💤 {date_key} 생성 전 충분히 대기 중 (12초)...")
            time.sleep(12) 
            
            print(f"🚀 {date_key} 생성 시도 중...")
            
            # [최적화] 입력 토큰 양을 줄이기 위해 내용을 3,000자로 대폭 제한합니다.
            summary_content = content[:3000]
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"다음 내용을 바탕으로 핵심 퀴즈 5문제만 만드세요. 정답은 <details>로 가리세요: \n\n {summary_content}"
            )
            
            if response and response.text:
                quiz_db[date_key] = response.text
                print(f"✅ {date_key} 생성 성공!")
            
        except Exception as e:
            # 에러 발생 시 30초를 더 쉬고 다음 파일로 넘어갑니다 (할당량 회복 시간 벌기)
            print(f"❌ {date_key} 실패: {e}")
            quiz_db[date_key] = f"할당량 초과로 생성 실패. 잠시 후 다시 시도하세요."
            time.sleep(30)

    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_quizzes()
