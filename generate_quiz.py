import google.generativeai as genai
import os
import glob
import json

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def generate_quizzes():
    md_files = glob.glob('./*.md')
    quiz_db = {}

    for file_path in md_files:
        date_key = os.path.basename(file_path).replace('.md', '')
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # AI에게 10문제 생성 요청 (비밀번호 인증 후 보여줄 내용)
            prompt = f"다음 학습 내용을 바탕으로 코딩 주관식을 포함한 10문제를 만드세요: {content}"
            quiz_db[date_key] = model.generate_content(prompt).text

    # 생성된 모든 퀴즈를 하나의 JSON으로 저장
    with open('quiz_db.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_db, f, ensure_ascii=False)

if __name__ == "__main__":
    generate_quizzes()
