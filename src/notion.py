import os
import requests
import json
from dotenv import load_dotenv
from src.parser import parse_text_and_math

# 현재 스크립트(notion.py) 위치를 기준으로 상위 폴더의 .env 절대 경로 찾기
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(current_dir), '.env')
load_dotenv(dotenv_path=env_path)

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
PAGE_ID = os.getenv('NOTION_PAGE_ID')

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_toggle_block(prompt, response_text):
    if not NOTION_TOKEN or not PAGE_ID:
        raise ValueError("❌ 환경변수 오류: .env 파일에 토큰과 페이지 ID가 없습니다.")

    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
    
    # parser.py의 함수 사용
    parsed_rich_text = parse_text_and_math(response_text)
    
    payload = {
        "children": [
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"type": "text", "text": {"content": f"❓ {prompt}"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {"rich_text": parsed_rich_text}
                        }
                    ]
                }
            }
        ]
    }
    
    response = requests.patch(url, headers=HEADERS, data=json.dumps(payload))
    
    if response.status_code == 200:
        return True
    else:
        raise Exception(f"API 요청 실패 (상태 코드: {response.status_code})\n{response.text}")