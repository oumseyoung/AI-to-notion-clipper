import re

# 노션 API가 공식적으로 지원하는 코드 블록 언어 목록
VALID_LANGUAGES = {"abap", "arduino", "bash", "basic", "c", "clojure", "coffeescript", "c++", "c#", "css", "dart", "diff", "docker", "elixir", "elm", "erlang", "flow", "fortran", "f#", "gherkin", "glsl", "go", "graphql", "groovy", "haskell", "html", "java", "javascript", "json", "julia", "kotlin", "latex", "less", "lisp", "livescript", "lua", "makefile", "markdown", "markup", "matlab", "mermaid", "nix", "objective-c", "ocaml", "pascal", "perl", "php", "plain text", "powershell", "prolog", "protobuf", "python", "r", "reason", "ruby", "rust", "sass", "scala", "scheme", "scss", "shell", "sql", "swift", "typescript", "vb.net", "verilog", "vhdl", "visual basic", "webassembly", "xml", "yaml"}

def parse_rich_text(text):
    """텍스트 내의 수식($), 굵은 글씨(**), 인라인 코드(`)를 노션 rich_text 포맷으로 변환"""
    pattern = r'(\$\$.*?\$\$|\$.*?\$|\*\*.*?\*\*|`.*?`)'
    parts = re.split(pattern, text)
    
    rich_text_array = []
    for part in parts:
        if not part: continue
            
        if part.startswith('$$') and part.endswith('$$'):
            rich_text_array.append({"type": "equation", "equation": {"expression": part.strip('$')}})
        elif part.startswith('$') and part.endswith('$'):
            rich_text_array.append({"type": "equation", "equation": {"expression": part.strip('$')}})
        elif part.startswith('**') and part.endswith('**'):
            rich_text_array.append({
                "type": "text", 
                "text": {"content": part[2:-2]},
                "annotations": {"bold": True}
            })
        elif part.startswith('`') and part.endswith('`'):
            rich_text_array.append({
                "type": "text", 
                "text": {"content": part[1:-1]},
                "annotations": {"code": True}
            })
        else:
            for i in range(0, len(part), 2000): # 2000자 제한 방어
                rich_text_array.append({"type": "text", "text": {"content": part[i:i+2000]}})
                
    return rich_text_array

def create_notion_block(block_type, text):
    """일반 텍스트를 특정 노션 블록으로 감싸는 헬퍼 함수"""
    return {
        "object": "block",
        "type": block_type,
        block_type: {
            "rich_text": parse_rich_text(text)
        }
    }

def markdown_to_notion_blocks(text):
    """전체 마크다운 텍스트를 분석하여 노션 블록 리스트로 반환"""
    blocks = []
    lines = text.split('\n')
    in_code_block = False
    code_content = []
    code_language = "plain text"
    
    for line in lines:
        # 1. 코드 블록(```) 처리
        if line.strip().startswith('```'):
            if in_code_block:
                # 코드 블록 닫기
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": "\n".join(code_content)[:2000]}}],
                        "language": code_language
                    }
                })
                in_code_block = False
                code_content = []
            else:
                # 코드 블록 열기
                in_code_block = True
                lang = line.strip()[3:].strip().lower()
                # 단축어 매핑
                if lang == 'py': lang = 'python'
                elif lang == 'js': lang = 'javascript'
                elif lang == 'ts': lang = 'typescript'
                elif lang == 'cpp': lang = 'c++'
                elif lang == 'sh': lang = 'shell'
                
                code_language = lang if lang in VALID_LANGUAGES else "plain text"
            continue
            
        if in_code_block:
            code_content.append(line)
            continue
            
        stripped_line = line.strip()
        if not stripped_line:
            continue
            
        # 2. 블록 수식($$) 단독 줄 처리
        if stripped_line.startswith('$$') and stripped_line.endswith('$$'):
            blocks.append({
                "object": "block",
                "type": "equation",
                "equation": {"expression": stripped_line.strip('$')}
            })
            continue
            
        # 3. 마크다운 기호에 따른 노션 블록 매핑
        if stripped_line.startswith('# '):
            blocks.append(create_notion_block("heading_1", stripped_line[2:]))
        elif stripped_line.startswith('## '):
            blocks.append(create_notion_block("heading_2", stripped_line[3:]))
        elif stripped_line.startswith('### '):
            blocks.append(create_notion_block("heading_3", stripped_line[4:]))
        elif stripped_line.startswith('- ') or stripped_line.startswith('* '):
            blocks.append(create_notion_block("bulleted_list_item", stripped_line[2:]))
        elif re.match(r'^\d+\.\s', stripped_line):
            # 숫자 목록 (예: "1. 텍스트")
            content = re.sub(r'^\d+\.\s+', '', stripped_line)
            blocks.append(create_notion_block("numbered_list_item", content))
        elif stripped_line.startswith('> '):
            blocks.append(create_notion_block("quote", stripped_line[2:]))
        else:
            # 기본 단락
            blocks.append(create_notion_block("paragraph", stripped_line))
            
    return blocks