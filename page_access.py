#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from notion_helper import NotionHelper

def main():
    notion = NotionHelper()
    
    # Get command center page ID from environment variable
    command_center_id = os.environ.get('COMMAND_CENTER_PAGE_ID', '')
    
    # Use COMMAND_CENTER_PAGE_ID if set, otherwise fallback to INFO_DUMP_PAGE_ID
    page_id = command_center_id
    
    if not page_id:
        print('{"items": [{"title": "Configuration needed", "subtitle": "Set COMMAND_CENTER_PAGE_ID in page_access.py or INFO_DUMP_PAGE_ID in workflow", "valid": false}]}')
        return
    
    # Always just open the command center page
    url = notion.get_page_url(page_id)
    print(f'{{"items": [{{"title": "🏠 Open Notion Command Center", "subtitle": "Press Enter to open your main page", "arg": "{url}", "valid": true}}]}}')

if __name__ == "__main__":
    main()