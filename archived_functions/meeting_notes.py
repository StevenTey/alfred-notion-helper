#!/usr/bin/env python3

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from notion_helper import NotionHelper

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    notion = NotionHelper()
    
    if not notion.meeting_notes_parent_id:
        print('{"items": [{"title": "Configuration needed", "subtitle": "Set MEETING_NOTES_PARENT_ID in workflow settings", "valid": false}]}')
        return
    
    # Generate meeting title with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if query.strip():
        meeting_title = f"Meeting: {query} - {timestamp}"
        subtitle = f"Create meeting note: {query}"
    else:
        meeting_title = f"Meeting - {timestamp}"
        subtitle = "Create timestamped meeting note"
    
    print(f'{{"items": [{{"title": "📝 {subtitle}", "subtitle": "Press Enter to create in Notion", "arg": "{meeting_title}", "valid": true}}]}}')

def create_meeting_note():
    """Called when user presses Enter"""
    meeting_title = sys.argv[1] if len(sys.argv) > 1 else f"Meeting - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    notion = NotionHelper()
    
    # Create meeting template content
    template_content = f"""# Attendees
- 

# Agenda
- 

# Notes


# Action Items
- [ ] 

# Next Steps
- 

---
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""
    
    try:
        result = notion.create_page(
            parent_id=notion.meeting_notes_parent_id,
            title=meeting_title,
            content=template_content
        )
        
        if 'id' in result:
            page_url = notion.get_page_url(result['id'])
            print(f"✅ Meeting note created: {meeting_title}")
            # Could also open the page automatically
            os.system(f'open "{page_url}"')
        else:
            print("❌ Failed to create meeting note")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        create_meeting_note()
    else:
        main()