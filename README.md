# Alfred Notion Helper

A powerful Alfred workflow that eliminates friction when working with Notion. Create shortcuts for common Notion actions without leaving Alfred.

## Features

🚀 **5 Core Shortcuts** to enhance your Notion workflow:

1. **📋 Clipboard Dump** - Hotkey to instantly dump clipboard content to your Notion info page with timestamp
2. **✅ Quick Tasks** - `nt` keyword to create tasks in your Notion database
3. **🔍 Page Access** - `np` keyword to search and open Notion pages directly  
4. **📝 Meeting Notes** - `nm` keyword to create timestamped meeting notes with template
5. **📔 Daily Journal** - `nj` keyword to add entries to your daily journal

## Why This Workflow?

Tired of manually opening Notion → navigating → creating pages? This workflow brings Notion actions directly to Alfred, saving clicks and eliminating context switching.

## Quick Setup

1. **Get Notion Token**: Create a [Notion integration](https://developers.notion.com/docs/getting-started) and copy your token
2. **Import Workflow**: Follow detailed setup in [`setup_instructions.md`](setup_instructions.md)
3. **Configure**: Set your token and page/database IDs in Alfred workflow settings
4. **Start Using**: Copy text + hotkey, or type `nt`, `np`, `nm`, `nj` + your content

## Usage Examples

```
# Quick task creation
nt Buy groceries
nt Call client about project update

# Page search & open
np project notes
np meeting agenda

# Meeting notes
nm Weekly standup
nm Client review session  

# Daily journal
nj Had a productive day working on the new feature
nj Learned about Alfred workflow development

# Clipboard dump (just copy text and press your hotkey)
```

## Requirements

- Alfred 4+ with Powerpack
- macOS
- Python 3
- Notion account with integration token

## Installation

1. Clone this repository
2. Install dependencies: `pip3 install -r requirements.txt`  
3. Follow the complete setup guide in [`setup_instructions.md`](setup_instructions.md)

## File Structure

- `notion_helper.py` - Core Notion API integration
- `clipboard_dump.py` - Clipboard dump functionality
- `quick_task.py` - Task creation with `nt` keyword
- `page_access.py` - Page search with `np` keyword  
- `meeting_notes.py` - Meeting notes with `nm` keyword
- `daily_journal.py` - Journal entries with `nj` keyword

## Configuration

Set these environment variables in your Alfred workflow:

- `NOTION_TOKEN` - Your Notion integration token
- `INFO_DUMP_PAGE_ID` - Target page for clipboard dumps
- `TASK_DATABASE_ID` - Target database for tasks
- `MEETING_NOTES_PARENT_ID` - Parent page for meeting notes
- `DAILY_JOURNAL_PARENT_ID` - Parent page for journal entries

See [`setup_instructions.md`](setup_instructions.md) for detailed configuration steps.

## Contributing

Feel free to submit issues, feature requests, or pull requests. Keep it simple and focused on reducing friction.

## License

MIT License - feel free to use and modify as needed.