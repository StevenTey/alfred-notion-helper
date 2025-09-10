#!/usr/bin/env python3

import sys
import os
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(__file__))
from notion_helper import NotionHelper

def sync_meetings(today_only=False):
    """Generate meeting notes from existing Notion database entries"""
    notion = NotionHelper()
    
    # Check required configuration
    if not all([notion.meetings_database_id, notion.meeting_template_page_id, notion.meeting_notes_parent_id]):
        return {
            "error": "Missing required environment variables: MEETINGS_DATABASE_ID, MEETING_TEMPLATE_PAGE_ID, MEETING_NOTES_PARENT_ID"
        }
    
    try:
        # Get meetings from database for the specified time period
        today = datetime.now().date()
        
        if today_only:
            start_date = today
            end_date = today
        else:
            # Get from today onwards for this week
            start_date = today
            end_date = today + timedelta(days=6)  # Next 7 days
        
        # Filter meetings for the date range and not completed
        filter_obj = {
            "and": [
                {
                    "property": "Date",
                    "date": {
                        "on_or_after": start_date.isoformat()
                    }
                },
                {
                    "property": "Date", 
                    "date": {
                        "on_or_before": end_date.isoformat()
                    }
                },
                {
                    "property": "Status",
                    "select": {
                        "does_not_equal": "Completed"
                    }
                }
            ]
        }
        
        sorts = [
            {
                "property": "Date",
                "direction": "ascending"
            }
        ]
        
        meetings_result = notion.query_database(notion.meetings_database_id, filter_obj, sorts)
        meetings = meetings_result.get('results', [])
        
        # Statistics
        stats = {
            "meetings_found": len(meetings),
            "notes_created": 0,
            "cancelled_updated": 0,
            "skipped": 0,
            "errors": []
        }
        
        for meeting in meetings:
            try:
                # Extract meeting properties
                properties = meeting['properties']
                meeting_id = meeting['id']
                
                # Get meeting title
                title_prop = properties.get('Name') or properties.get('Title')
                if not title_prop:
                    notes_stats["errors"].append(f"Meeting {meeting_id}: No title property found")
                    continue
                    
                meeting_title = title_prop['title'][0]['text']['content'] if title_prop['title'] else "Untitled Meeting"
                
                # Get meeting date
                date_prop = properties.get('Date')
                if not date_prop or not date_prop['date']:
                    notes_stats["errors"].append(f"Meeting '{meeting_title}': No date found")
                    continue
                
                meeting_date = date_prop['date']['start']
                
                # Get status
                status_prop = properties.get('Status')
                status = status_prop['select']['name'] if status_prop and status_prop['select'] else "Scheduled"
                
                # Get notes generated flag
                notes_generated_prop = properties.get('Notes Generated')
                notes_generated = notes_generated_prop['checkbox'] if notes_generated_prop else False
                
                # Get meeting note page link
                note_page_prop = properties.get('Meeting Note Page')
                note_page_id = note_page_prop['relation'][0]['id'] if (note_page_prop and note_page_prop['relation']) else None
                
                # Process based on status and current state
                if status == "Cancelled":
                    # Update meeting note page title if exists
                    if note_page_id and not meeting_title.endswith("(Cancelled)"):
                        cancelled_title = f"{meeting_title} (Cancelled)"
                        notion.update_page_properties(note_page_id, {
                            "title": {
                                "title": [{"text": {"content": cancelled_title}}]
                            }
                        })
                        stats["cancelled_updated"] += 1
                    else:
                        stats["skipped"] += 1
                        
                elif status == "Scheduled" and not notes_generated:
                    # Create meeting note from template
                    formatted_date = datetime.fromisoformat(meeting_date.replace('Z', '+00:00')).strftime("%Y-%m-%d")
                    note_title = f"{meeting_title} - {formatted_date}"
                    
                    # Clone template page
                    new_page_result = notion.duplicate_page(
                        notion.meeting_template_page_id,
                        note_title,
                        notion.meeting_notes_parent_id
                    )
                    
                    if 'id' in new_page_result:
                        new_page_id = new_page_result['id']
                        
                        # Update meeting database entry
                        notion.update_page_properties(meeting_id, {
                            "Notes Generated": {"checkbox": True},
                            "Meeting Note Page": {
                                "relation": [{"id": new_page_id}]
                            }
                        })
                        
                        stats["notes_created"] += 1
                    else:
                        stats["errors"].append(f"Failed to create note for '{meeting_title}': {new_page_result}")
                        
                else:
                    stats["skipped"] += 1
                    
            except Exception as e:
                stats["errors"].append(f"Error processing meeting: {str(e)}")
        
        return stats
        
    except Exception as e:
        return {"error": f"Sync failed: {str(e)}"}

def main():
    """Alfred Script Filter interface"""
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    
    # Determine sync mode
    today_only = "today" in query.lower()
    mode = "today" if today_only else "week"
    
    print(f'{{"items": [{{"title": "🔄 Sync Meeting Notes ({mode})", "subtitle": "Press Enter to sync meeting notes from calendar", "arg": "{mode}", "valid": true}}]}}')

def run_sync():
    """Execute the sync operation"""
    mode = sys.argv[1] if len(sys.argv) > 1 else "week"
    today_only = mode == "today"
    
    print(f"🔄 Starting meeting sync ({mode})...")
    
    result = sync_meetings(today_only)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    # Print results
    print(f"✅ Meeting sync completed!")
    print(f"   Meetings found: {result['meetings_found']}")
    print(f"   Meeting notes created: {result['notes_created']}")
    print(f"   Cancelled meetings updated: {result['cancelled_updated']}")  
    print(f"   Skipped: {result['skipped']}")
    
    if result['errors']:
        print(f"   Errors: {len(result['errors'])}")
        for error in result['errors']:
            print(f"   • {error}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sync":
        run_sync()
    else:
        main()