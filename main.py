import sys
from src.notion import create_toggle_block

def main():
    # 표준 입력(stdin)으로 터미널의 모든 텍스트를 한 번에 안전하게 읽어옵니다.
    raw_input = sys.stdin.read()
    
    # 지정한 구분자(===DELIMITER===)를 기준으로 질문과 답변을 분리합니다.
    if "===DELIMITER===" not in raw_input:
        print("❌ 오류: 데이터를 올바르게 전달받지 못했습니다.")
        sys.exit(1)
        
    parts = raw_input.split("===DELIMITER===")
    user_prompt = parts[0].strip()
    gemini_response = parts[1].strip()
    
    try:
        print("⏳ 노션으로 데이터를 전송 중입니다...")
        create_toggle_block(user_prompt, gemini_response)
        print("✅ 성공: 토글과 내용이 노션에 안전하게 저장되었습니다!")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()