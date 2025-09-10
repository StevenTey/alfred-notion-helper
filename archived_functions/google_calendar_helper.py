#!/usr/bin/env python3

import os
import json
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GoogleCalendarHelper:
    def __init__(self):
        # Scopes required for reading calendar events
        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        
        # Credentials file paths (to be set via environment variables)
        self.credentials_file = os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        self.token_file = os.environ.get('GOOGLE_TOKEN_FILE', 'token.json')
        
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Check if token file exists (stores user's access and refresh tokens)
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(f"Google credentials file not found: {self.credentials_file}")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)

    def get_todays_events(self, calendar_id='primary'):
        """Get today's calendar events"""
        return self.get_events_for_date_range(
            start_date=datetime.now().date(),
            end_date=datetime.now().date(),
            calendar_id=calendar_id
        )

    def get_this_weeks_events(self, from_today_only=False, calendar_id='primary'):
        """Get this week's calendar events (from today onwards if specified)"""
        today = datetime.now().date()
        
        if from_today_only:
            start_date = today
        else:
            # Get start of this week (Monday)
            start_date = today - timedelta(days=today.weekday())
        
        end_date = start_date + timedelta(days=6)  # End of week
        
        return self.get_events_for_date_range(start_date, end_date, calendar_id)

    def get_events_for_date_range(self, start_date, end_date, calendar_id='primary'):
        """Get calendar events for a specific date range"""
        if not self.service:
            raise Exception("Google Calendar service not initialized")

        # Convert dates to RFC3339 format
        start_datetime = datetime.combine(start_date, datetime.min.time()).isoformat() + 'Z'
        end_datetime = datetime.combine(end_date, datetime.max.time()).isoformat() + 'Z'

        try:
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=start_datetime,
                timeMax=end_datetime,
                maxResults=50,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Process events into a standardized format
            processed_events = []
            for event in events:
                processed_event = self._process_event(event)
                if processed_event:
                    processed_events.append(processed_event)
            
            return processed_events
            
        except Exception as e:
            raise Exception(f"Failed to fetch Google Calendar events: {str(e)}")

    def _process_event(self, event):
        """Process raw Google Calendar event into standardized format"""
        try:
            # Extract basic event info
            event_id = event.get('id', '')
            summary = event.get('summary', 'Untitled Meeting')
            status = event.get('status', 'confirmed')  # confirmed, tentative, cancelled
            
            # Extract start time
            start = event.get('start', {})
            if 'dateTime' in start:
                start_datetime = datetime.fromisoformat(start['dateTime'].replace('Z', '+00:00'))
                is_all_day = False
            elif 'date' in start:
                start_datetime = datetime.fromisoformat(start['date'] + 'T00:00:00')
                is_all_day = True
            else:
                return None  # Skip events without valid start time
            
            # Extract end time
            end = event.get('end', {})
            if 'dateTime' in end:
                end_datetime = datetime.fromisoformat(end['dateTime'].replace('Z', '+00:00'))
            elif 'date' in end:
                end_datetime = datetime.fromisoformat(end['date'] + 'T23:59:59')
            else:
                end_datetime = start_datetime + timedelta(hours=1)  # Default 1 hour
            
            # Extract attendees
            attendees = []
            for attendee in event.get('attendees', []):
                attendee_info = {
                    'email': attendee.get('email', ''),
                    'name': attendee.get('displayName', attendee.get('email', '')),
                    'status': attendee.get('responseStatus', 'needsAction')
                }
                attendees.append(attendee_info)
            
            # Extract other details
            description = event.get('description', '')
            location = event.get('location', '')
            
            return {
                'id': event_id,
                'title': summary,
                'start_datetime': start_datetime,
                'end_datetime': end_datetime,
                'date': start_datetime.date(),
                'is_all_day': is_all_day,
                'status': self._map_google_status_to_notion(status),
                'description': description,
                'location': location,
                'attendees': attendees,
                'google_event_id': event_id,
                'last_updated': datetime.now()
            }
            
        except Exception as e:
            print(f"Warning: Failed to process event {event.get('id', 'unknown')}: {str(e)}")
            return None

    def _map_google_status_to_notion(self, google_status):
        """Map Google Calendar status to Notion status"""
        status_mapping = {
            'confirmed': 'Scheduled',
            'tentative': 'Scheduled', 
            'cancelled': 'Cancelled'
        }
        return status_mapping.get(google_status, 'Scheduled')