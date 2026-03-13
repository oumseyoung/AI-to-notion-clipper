import sys
from src.notion import create_toggle_block

def main():
    # 외부(단축어/터미널)에서 2개의 인자를 받아옴
    if len(sys.argv) < 3:
        print("❌ 사용법: python main.py '<프롬프트>' '<제미나이 답변>'")
        sys.exit(1)
        
    user_prompt = sys.argv[1]
    gemini_response = sys.argv[2]
    
    try:
        print("⏳ 노션으로 데이터를 전송 중입니다...")
        create_toggle_block(user_prompt, gemini_response)
        print("✅ 성공: 토글과 수식이 노션에 안전하게 저장되었습니다!")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()