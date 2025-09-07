#!/usr/bin/env python3

import os
import sys
import json
import requests
from datetime import datetime

class NotionHelper:
    def __init__(self):
        # Get token from Alfred workflow environment variables
        self.token = os.environ.get('NOTION_TOKEN', '')
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Page/Database IDs (to be configured)
        self.info_dump_page_id = os.environ.get('INFO_DUMP_PAGE_ID', '')
        self.task_database_id = os.environ.get('TASK_DATABASE_ID', '')
        self.meeting_notes_parent_id = os.environ.get('MEETING_NOTES_PARENT_ID', '')
        self.daily_journal_parent_id = os.environ.get('DAILY_JOURNAL_PARENT_ID', '')

    def create_page(self, parent_id, title, content=""):
        """Create a new page under a parent page"""
        url = "https://api.notion.com/v1/pages"
        
        data = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            }
        }
        
        if content:
            data["children"] = [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                }
            ]
        
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def append_to_page(self, page_id, content):
        """Append content to an existing page"""
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        
        data = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                }
            ]
        }
        
        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()

    def create_task(self, title, description=""):
        """Create a task in the task database"""
        url = "https://api.notion.com/v1/pages"
        
        data = {
            "parent": {"database_id": self.task_database_id},
            "properties": {
                "Task": {
                    "title": [{"text": {"content": title}}]
                }
            }
        }
        
        if description:
            data["children"] = [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": description}}]
                    }
                }
            ]
        
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def search_pages(self, query):
        """Search for pages matching query"""
        url = "https://api.notion.com/v1/search"
        
        data = {
            "query": query,
            "filter": {
                "value": "page",
                "property": "object"
            },
            "sort": {
                "direction": "descending",
                "timestamp": "last_edited_time"
            }
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def get_page_url(self, page_id):
        """Get the Notion URL for a page"""
        # Remove any dashes and ensure proper format
        clean_id = page_id.replace('-', '')
        return f"https://www.notion.so/{clean_id}"