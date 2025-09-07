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
    notion = NotionHelper()
    
    # Get clipboard content
    clipboard_content = get_clipboard()
    
    if not clipboard_content.strip():
        print('{"items": [{"title": "No clipboard content", "subtitle": "Copy some text first", "valid": false}]}')
        return
    
    if not notion.info_dump_page_id:
        print('{"items": [{"title": "Configuration needed", "subtitle": "Set INFO_DUMP_PAGE_ID in workflow settings", "valid": false}]}')
        return
    
    # Prepare content with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"[{timestamp}]\n{clipboard_content}"
    
    try:
        # Append to info dump page
        result = notion.append_to_page(notion.info_dump_page_id, content)
        
        if 'id' in result:
            print('{"items": [{"title": "✅ Dumped to Notion", "subtitle": "Clipboard content added successfully", "valid": false}]}')
        else:
            print('{"items": [{"title": "❌ Failed to dump", "subtitle": "Check your configuration", "valid": false}]}')
    
    except Exception as e:
        print(f'{{"items": [{{"title": "❌ Error", "subtitle": "{str(e)}", "valid": false}}]}}')

if __name__ == "__main__":
    main()