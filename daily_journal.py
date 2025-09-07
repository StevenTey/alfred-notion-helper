#!/usr/bin/env python3

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from notion_helper import NotionHelper

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    notion = NotionHelper()
    
    if not notion.daily_journal_parent_id:
        print('{"items": [{"title": "Configuration needed", "subtitle": "Set DAILY_JOURNAL_PARENT_ID in workflow settings", "valid": false}]}')
        return
    
    if not query.strip():
        print('{"items": [{"title": "Add to daily journal", "subtitle": "Type your journal entry and press Enter", "valid": false}]}')
        return
    
    # Show what will be added
    today = datetime.now().strftime("%Y-%m-%d")
    print(f'{{"items": [{{"title": "📔 Add to journal ({today})", "subtitle": "Entry: {query[:50]}...", "arg": "{query}", "valid": true}}]}}')

def add_to_journal():
    """Called when user presses Enter"""
    entry_content = sys.argv[1] if len(sys.argv) > 1 else ""
    notion = NotionHelper()
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_title = f"Journal - {today}"
    timestamp = datetime.now().strftime("%H:%M")
    
    # First, try to find today's journal page
    try:
        search_result = notion.search_pages(today_title)
        today_page = None
        
        for page in search_result.get('results', []):
            page_title = ""
            if page.get('properties', {}).get('title', {}).get('title'):
                page_title = page['properties']['title']['title'][0]['text']['content']
            
            if page_title == today_title:
                today_page = page
                break
        
        if today_page:
            # Append to existing page
            content = f"**{timestamp}** - {entry_content}"
            result = notion.append_to_page(today_page['id'], content)
            print(f"✅ Added to today's journal ({today})")
        else:
            # Create new journal page for today
            initial_content = f"# Daily Journal - {today}\n\n**{timestamp}** - {entry_content}"
            result = notion.create_page(
                parent_id=notion.daily_journal_parent_id,
                title=today_title,
                content=initial_content
            )
            print(f"✅ Created new journal for {today}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--add":
        add_to_journal()
    else:
        main()