import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from src.parser import markdown_to_notion_blocks, parse_rich_text

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
        raise ValueError("❌ Environment variable error: NOTION_TOKEN or NOTION_PAGE_ID is missing in the .env file.")

    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 질문(Prompt)을 보기 좋은 회색 콜아웃(Callout) 블록으로 디자인
    prompt_block = {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": parse_rich_text(prompt),
            "icon": {"type": "emoji", "emoji": "🙋‍♂️"},
            "color": "gray_background"
        }
    }
    
    # 답변(Response) 마크다운을 노션 블록 리스트로 완벽 변환
    response_blocks = markdown_to_notion_blocks(response_text)
    
    # 노션 API는 한 번에 최대 100개의 블록만 추가 가능하므로, 질문 블록 1개 + 답변 블록 최대 98개로 자르기
    toggle_children = [prompt_block] + response_blocks[:98]
    
    payload = {
        "children": [
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"type": "text", "text": {"content": f"🕒 {current_time}"}}],
                    "children": toggle_children
                }
            }
        ]
    }
    
    response = requests.patch(url, headers=HEADERS, data=json.dumps(payload))
    
    if response.status_code == 200:
        return True
    else:
        raise Exception(f"API request failed (Status Code: {response.status_code})\n{response.text}")