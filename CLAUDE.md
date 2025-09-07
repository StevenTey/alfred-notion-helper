# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Alfred workflow project for integrating with Notion. Creates 5 core shortcuts to eliminate friction when working with Notion through Alfred.

**Current Status**: Core implementation complete. All 5 features implemented and ready for Alfred configuration.

**Core Features**:
1. **Clipboard Dump** - Hotkey to dump clipboard content to Notion info page with timestamp
2. **Quick Task Creation** - `nt` keyword to instantly create tasks in Notion database  
3. **Page Search & Access** - `np` keyword to search and open Notion pages directly
4. **Meeting Notes** - `nm` keyword to create timestamped meeting notes with template
5. **Daily Journal** - `nj` keyword to add entries to daily journal pages

## Important Instructions
- Think Hard very hard.

## Core Workflow: Research → Plan → Implement → Validate
Start every feature with: "Let me research the codebase and create a plan before implementing."

- Research - Understand existing patterns and architecture
- Plan - Propose approach and verify with you
- Implement - Build with tests and error handling
- Validate - ALWAYS run formatters, linters, and tests after implementation

## Code Organization
Keep functions small and focused:

- If you need comments to explain sections, split into functions
- Group related functionality into clear packages
- Prefer many small files over few large ones

## Problem Solving
- When stuck: Stop. The simple solution is usually correct.
- When uncertain: "Let me ultrathink about this architecture."
- When choosing: "I see approach A (simple) vs B (flexible). Which do you prefer?"
- Your redirects prevent over-engineering. When uncertain about implementation, stop and ask for guidance.

## Architecture

**Technology Stack**:
- Python 3 scripts for all Notion API interactions
- `requests` library for HTTP calls to Notion API
- Alfred Script Filters for user interface
- Environment variables for secure token storage

**File Structure**:
- `notion_helper.py` - Core Notion API integration class
- `clipboard_dump.py` - Hotkey-triggered clipboard dump functionality  
- `quick_task.py` - Task creation with `nt` keyword
- `page_access.py` - Page search/open with `np` keyword
- `meeting_notes.py` - Meeting note creation with `nm` keyword
- `daily_journal.py` - Journal entry with `nj` keyword
- `setup_instructions.md` - Complete Alfred workflow setup guide

**API Integration**:
- Uses official Notion API v2022-06-28
- Requires Notion integration token with appropriate page/database permissions
- Handles page creation, content appending, database entries, and search

## Configuration Requirements

**Required Environment Variables** (set in Alfred workflow):
- `NOTION_TOKEN` - Notion integration token
- `INFO_DUMP_PAGE_ID` - Target page for clipboard dumps
- `TASK_DATABASE_ID` - Target database for tasks  
- `MEETING_NOTES_PARENT_ID` - Parent page for meeting notes
- `DAILY_JOURNAL_PARENT_ID` - Parent page for journal entries

**Alfred Setup**:
Each Python script corresponds to a Script Filter in Alfred with specific keywords and actions. See `setup_instructions.md` for detailed configuration steps.

## Development Workflow

**When making changes**:
1. Test individual Python scripts from command line first
2. Update Alfred workflow configuration if adding new features
3. Verify all environment variables are properly set
4. Test each feature through Alfred interface

**Common Development Tasks**:
- **Testing scripts**: `python3 script_name.py "test input"`
- **Debugging**: Check Alfred's workflow debugger for error output
- **Adding features**: Follow existing pattern in `notion_helper.py`

**User's Preferences**:
- Prioritize simplicity over complexity
- Focus on reducing friction in daily Notion workflow  
- No over-engineering - keep solutions straightforward
- Enhance shortcut capabilities rather than replace existing tools

## Git Configuration

Repository on `master` branch. Current implementation is feature-complete for the 5 core actions.