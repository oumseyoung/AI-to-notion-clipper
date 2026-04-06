import re

def parse_text_and_math(text):
    # $$수식$$ (블록 수식) 또는 $수식$ (인라인 수식)을 찾아내는 정규식
    pattern = r'(\$\$.*?\$\$|\$.*?\$)'
    parts = re.split(pattern, text, flags=re.DOTALL)
    
    rich_text_array = []
    
    for part in parts:
        if not part:
            continue
            
        if part.startswith('$$') and part.endswith('$$'):
            expression = part.strip('$').strip()
            rich_text_array.append({
                "type": "equation",
                "equation": {"expression": expression}
            })
        elif part.startswith('$') and part.endswith('$'):
            expression = part.strip('$').strip()
            rich_text_array.append({
                "type": "equation",
                "equation": {"expression": expression}
            })
        else:
            # 텍스트가 길 경우 노션 API 제한(2000자)을 피하기 위해 쪼개기
            for i in range(0, len(part), 2000):
                rich_text_array.append({
                    "type": "text",
                    "text": {"content": part[i:i+2000]}
                })
            
    return rich_text_array