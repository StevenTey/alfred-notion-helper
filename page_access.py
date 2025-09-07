#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from notion_helper import NotionHelper

# Set your main command center page ID here
COMMAND_CENTER_PAGE_ID = "1cc172ec83638026ab3bc4fd3c7e0db1"  # Replace with your main Notion page ID

def main():
    notion = NotionHelper()
    
    # Use INFO_DUMP_PAGE_ID if COMMAND_CENTER_PAGE_ID is not set
    page_id = COMMAND_CENTER_PAGE_ID or notion.info_dump_page_id
    
    if not page_id:
        print('{"items": [{"title": "Configuration needed", "subtitle": "Set COMMAND_CENTER_PAGE_ID in page_access.py or INFO_DUMP_PAGE_ID in workflow", "valid": false}]}')
        return
    
    # Always just open the command center page
    url = notion.get_page_url(page_id)
    print(f'{{"items": [{{"title": "🏠 Open Notion Command Center", "subtitle": "Press Enter to open your main page", "arg": "{url}", "valid": true}}]}}')

if __name__ == "__main__":
    main()