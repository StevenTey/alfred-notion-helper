#!/usr/bin/env python3

import sys
import os
import subprocess
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from notion_helper import NotionHelper

def get_clipboard():
    """Get text from clipboard"""
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        return result.stdout
    except:
        return ""

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    notion = NotionHelper()
    
    if not notion.info_dump_page_id:
        print('{"items": [{"title": "Configuration needed", "subtitle": "Set INFO_DUMP_PAGE_ID in workflow settings", "valid": false}]}')
        return
    
    # Use typed text if provided, otherwise use clipboard
    if query.strip():
        content = query.strip()
        source = "typed text"
    else:
        content = get_clipboard()
        source = "clipboard"
    
    if not content.strip():
        print('{"items": [{"title": "No content to dump", "subtitle": "Type something or copy text to clipboard first", "valid": false}]}')
        return
    
    # Show preview of what will be dumped
    preview = content[:100] + "..." if len(content) > 100 else content
    # Escape quotes in preview
    preview = preview.replace('"', '\\"').replace('\n', ' ')
    print(f'{{"items": [{{"title": "📝 Dump {source} to Notion", "subtitle": "Preview: {preview}", "arg": "{content}", "valid": true}}]}}')

def dump_content():
    """Actually dump the content"""
    # Debug: print all arguments to see what we're getting
    print(f"DEBUG: sys.argv = {sys.argv}", file=sys.stderr)
    
    # The content should be in sys.argv[2] after --dump
    content_to_dump = sys.argv[2] if len(sys.argv) > 2 else ""
    notion = NotionHelper()
    
    print(f"DEBUG: content_to_dump = '{content_to_dump}'", file=sys.stderr)
    
    # If no argument passed, try to get from clipboard
    if not content_to_dump.strip():
        content_to_dump = get_clipboard()
        print(f"DEBUG: using clipboard = '{content_to_dump}'", file=sys.stderr)
    
    if not content_to_dump.strip():
        print("❌ No content to dump")
        return
    
    # Prepare content with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"[{timestamp}]\n{content_to_dump}"
    
    try:
        # Append to info dump page
        result = notion.append_to_page(notion.info_dump_page_id, content)
        
        if 'id' in result:
            print("✅ Content dumped to Notion successfully")
        else:
            print(f"❌ Failed to dump: {result}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--dump":
        dump_content()
    else:
        main()