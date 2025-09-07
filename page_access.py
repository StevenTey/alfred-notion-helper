#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from notion_helper import NotionHelper

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    notion = NotionHelper()
    
    if not query.strip():
        print('{"items": [{"title": "Search Notion pages", "subtitle": "Type to search your pages", "valid": false}]}')
        return
    
    try:
        results = notion.search_pages(query)
        
        if not results.get('results'):
            print('{"items": [{"title": "No pages found", "subtitle": "Try a different search term", "valid": false}]}')
            return
        
        items = []
        for page in results['results'][:10]:  # Limit to 10 results
            title = "Untitled"
            if page.get('properties', {}).get('title', {}).get('title'):
                title = page['properties']['title']['title'][0]['text']['content']
            elif page.get('properties', {}).get('Name', {}).get('title'):
                title = page['properties']['Name']['title'][0]['text']['content']
            
            page_url = notion.get_page_url(page['id'])
            
            items.append({
                "title": title,
                "subtitle": f"Open in Notion • {page['last_edited_time'][:10]}",
                "arg": page_url,
                "valid": True
            })
        
        print('{"items": ' + str(items).replace("'", '"') + '}')
    
    except Exception as e:
        print(f'{{"items": [{{"title": "❌ Search error", "subtitle": "{str(e)}", "valid": false}}]}}')

if __name__ == "__main__":
    main()