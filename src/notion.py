import os
import requests
import json
from dotenv import load_dotenv
from src.parser import parse_text_and_math

# .env 파일 로드
load_dotenv()
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