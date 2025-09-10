# Alfred-Notion Helper Setup Instructions

## 1. Create Alfred Workflow

1. Open Alfred Preferences > Workflows
2. Click "+" > Templates > Essentials > Keyword to Script
3. Name it "Notion Helper"
4. Replace the default script files with the ones from this project

## 2. Configure Workflow Variables

In Alfred workflow settings, add these environment variables:

- `NOTION_TOKEN`: Your Notion integration token
- `INFO_DUMP_PAGE_ID`: Page ID where clipboard dumps go
- `TASK_DATABASE_ID`: Database ID for your tasks
- `MEETING_NOTES_PARENT_ID`: Parent page ID for meeting notes  
- `DAILY_JOURNAL_PARENT_ID`: Parent page ID for daily journals
- `MEETINGS_DATABASE_ID`: Database ID for storing meeting entries
- `MEETING_TEMPLATE_PAGE_ID`: Template page ID to clone for meeting notes

## 3. Set Up Script Filters

Create 6 Script Filters with these settings:

### 1. Clipboard Dump (Hotkey)
- **Type**: Hotkey (no keyword needed)
- **Hotkey**: Choose your preferred hotkey (e.g., ⌥⌘V)
- **Script**: `/usr/bin/python3 clipboard_dump.py`
- **Action**: No action needed (just runs)

### 2. Quick Task 
- **Keyword**: `nt`
- **Script**: `/usr/bin/python3 quick_task.py {query}`
- **Action**: Run Script with input `{query}`
- **Action Script**: `/usr/bin/python3 quick_task.py --create {query}`

### 3. Page Access
- **Keyword**: `np`  
- **Script**: `/usr/bin/python3 page_access.py {query}`
- **Action**: Open URL `{query}`

### 4. Meeting Notes
- **Keyword**: `nm`
- **Script**: `/usr/bin/python3 meeting_notes.py {query}`
- **Action**: Run Script with input `{query}`
- **Action Script**: `/usr/bin/python3 meeting_notes.py --create {query}`

### 5. Daily Journal  
- **Keyword**: `nj`
- **Script**: `/usr/bin/python3 daily_journal.py {query}`
- **Action**: Run Script with input `{query}`  
- **Action Script**: `/usr/bin/python3 daily_journal.py --add {query}`

### 6. Meeting Sync
- **Keyword**: Choose your keyword (e.g., `msync` or `sync-meetings`)
- **Script**: `./meeting_sync_wrapper.sh {query}`
- **Action**: Run Script with input `{query}`
- **Action Script**: `./meeting_sync_wrapper.sh --sync {query}`

## 4. Get Notion IDs

### Page IDs:
1. Open the page in Notion
2. Copy the URL - the ID is the long string after the last slash
3. Example: `https://notion.so/My-Page-abc123def456` → ID is `abc123def456`

### Database IDs:
1. Open database in Notion  
2. Copy URL - same process as pages
3. Or use "Copy link to view" from the database menu

## 5. Database Setup (for Meeting Sync)

Your meetings database should have these columns:
- **Name** (title property) - Meeting name
- **Date** (date property) - Meeting date
- **Status** (select property) - Options: "Scheduled", "Completed", "Cancelled"
- **Notes Generated** (checkbox property) - Tracks if meeting note was created
- **Meeting Note Page** (relation property) - Links to the generated meeting note page
- **Description** (rich text property, optional) - Meeting description
- **Location** (rich text property, optional) - Meeting location

## 6. Calendar Integration Setup

**Recommended: Use Zapier (Free Plan)**
1. **Create Zapier account** (free plan includes 100 tasks/month)
2. **Create Zap**: Google Calendar (New Event) → Notion (Create Database Item)
3. **Map fields**: Event title → Name, Event date → Date, Set Status to "Scheduled"
4. **Test the integration** to ensure events sync properly

**Alternative**: Manually add meetings to your Notion database

## 8. Usage

- **Clipboard Dump**: Copy text, press your hotkey
- **Quick Task**: Type `nt` + your task  
- **Page Access**: Type `np` + search term
- **Meeting Notes**: Type `nm` + optional meeting name
- **Daily Journal**: Type `nj` + your journal entry
- **Meeting Sync**: Type your keyword + "today" for today only, or just keyword for this week
  - Reads meetings from your Notion database
  - Generates meeting notes from template for scheduled meetings
  - Handles cancelled meetings by updating note titles
  - Works with Zapier or manual database entries