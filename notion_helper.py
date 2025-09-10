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
        self.meetings_database_id = os.environ.get('MEETINGS_DATABASE_ID', '')
        self.meeting_template_page_id = os.environ.get('MEETING_TEMPLATE_PAGE_ID', '')

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

    def query_database(self, database_id, filter_obj=None, sorts=None):
        """Query database with optional filters and sorts"""
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        
        data = {}
        if filter_obj:
            data["filter"] = filter_obj
        if sorts:
            data["sorts"] = sorts
            
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def update_page_properties(self, page_id, properties):
        """Update properties of an existing page"""
        url = f"https://api.notion.com/v1/pages/{page_id}"
        
        data = {"properties": properties}
        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()

    def duplicate_page(self, template_page_id, new_title, parent_id):
        """Clone a template page with a new title under specified parent"""
        # First, get the template page content
        url = f"https://api.notion.com/v1/blocks/{template_page_id}/children"
        response = requests.get(url, headers=self.headers)
        template_blocks = response.json().get('results', [])
        
        # Create new page with template content
        create_url = "https://api.notion.com/v1/pages"
        data = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": new_title}}]
                }
            },
            "children": template_blocks
        }
        
        create_response = requests.post(create_url, headers=self.headers, json=data)
        return create_response.json()

    def create_or_update_meeting_entry(self, calendar_event):
        """Create or update a meeting entry in Notion database from calendar event"""
        # First, check if meeting already exists (by Google event ID)
        existing_meeting = self.find_meeting_by_google_id(calendar_event['google_event_id'])
        
        # Prepare properties for the meeting entry
        properties = {
            "Name": {
                "title": [{"text": {"content": calendar_event['title']}}]
            },
            "Date": {
                "date": {"start": calendar_event['date'].isoformat()}
            },
            "Status": {
                "select": {"name": calendar_event['status']}
            },
            "Google Event ID": {
                "rich_text": [{"text": {"content": calendar_event['google_event_id']}}]
            }
        }
        
        # Add optional properties if they exist
        if calendar_event.get('description'):
            properties["Description"] = {
                "rich_text": [{"text": {"content": calendar_event['description'][:2000]}}]  # Notion limit
            }
        
        if calendar_event.get('location'):
            properties["Location"] = {
                "rich_text": [{"text": {"content": calendar_event['location']}}]
            }
            
        if existing_meeting:
            # Update existing meeting
            result = self.update_page_properties(existing_meeting['id'], properties)
            return {'action': 'updated', 'result': result, 'meeting_id': existing_meeting['id']}
        else:
            # Create new meeting entry
            url = "https://api.notion.com/v1/pages"
            data = {
                "parent": {"database_id": self.meetings_database_id},
                "properties": properties
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            result = response.json()
            return {'action': 'created', 'result': result, 'meeting_id': result.get('id')}

    def find_meeting_by_google_id(self, google_event_id):
        """Find existing meeting in Notion database by Google event ID"""
        filter_obj = {
            "property": "Google Event ID",
            "rich_text": {
                "equals": google_event_id
            }
        }
        
        result = self.query_database(self.meetings_database_id, filter_obj)
        meetings = result.get('results', [])
        
        return meetings[0] if meetings else None

    def sync_calendar_events_to_database(self, calendar_events):
        """Sync multiple calendar events to Notion database"""
        sync_stats = {
            'created': 0,
            'updated': 0,
            'errors': []
        }
        
        for event in calendar_events:
            try:
                result = self.create_or_update_meeting_entry(event)
                if result['action'] == 'created':
                    sync_stats['created'] += 1
                else:
                    sync_stats['updated'] += 1
                    
            except Exception as e:
                sync_stats['errors'].append(f"Failed to sync event '{event['title']}': {str(e)}")
        
        return sync_stats