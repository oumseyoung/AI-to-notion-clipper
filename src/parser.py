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
            rich_text_array.append({
                "type": "text",
                "text": {"content": part}
            })
            
    return rich_text_array