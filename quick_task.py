#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from notion_helper import NotionHelper

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    notion = NotionHelper()
    
    if not query.strip():
        print('{"items": [{"title": "Add task to Notion", "subtitle": "Type your task and press Enter", "valid": false}]}')
        return
    
    if not notion.task_database_id:
        print('{"items": [{"title": "Configuration needed", "subtitle": "Set TASK_DATABASE_ID in workflow settings", "valid": false}]}')
        return
    
    # Show what will be created
    print(f'{{"items": [{{"title": "✅ Create task: {query}", "subtitle": "Press Enter to add to your task database", "arg": "{query}", "valid": true}}]}}')

def create_task():
    """Called when user presses Enter"""
    task_title = sys.argv[1] if len(sys.argv) > 1 else ""
    notion = NotionHelper()
    
    try:
        result = notion.create_task(task_title)
        if 'id' in result:
            print(f"✅ Task '{task_title}' created successfully")
        else:
            print("❌ Failed to create task")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        create_task()
    else:
        main()