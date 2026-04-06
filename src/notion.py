import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from src.parser import parse_text_and_math

# Find the absolute path of the .env file in the parent directory based on the current script location
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
    
    # 1. Get current date and time (e.g., 2026-04-06 22:56:56)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Parse the response text
    parsed_rich_text = parse_text_and_math(response_text)
    
    # 3. Construct Notion API payload (Toggle title: Time / Content: 2 bulleted list items)
    payload = {
        "children": [
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"type": "text", "text": {"content": f"🕒 {current_time}"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{"type": "text", "text": {"content": f"Q: {prompt}"}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": parsed_rich_text
                            }
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
        raise Exception(f"API request failed (Status Code: {response.status_code})\n{response.text}")