#!/usr/bin/env python
import pprint
from apiclient.discovery import build
from GoogleAPI import GetCredentials
from oauth2client.client import AccessTokenRefreshError
from datetime import datetime
from datetime import timedelta
from dateutil import parser


class GoogleCalendar:

    def __init__(self):
        """ 
        class contructor

        """
        self.authenticatedHTTP =  GetCredentials()
        self.service = build('calendar', 'v3', http=self.authenticatedHTTP)


    def fetchCalendars(self):
        """ fetch a list of calendars

        Args:
            param (class): self.

        Returns:
            void

        """
        request = self.service.calendarList().list()
        response = request.execute()
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(response.get('items', []))


    def todayEvents(self):
        """ get the events for current day

        Args:
            param (class): self.

        Returns:
            (dict) events

        """
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        end = datetime.now().strftime('%Y-%m-%d') + 'T23:59:59.951524Z'

        events =self.eventsByDate(now, end)
        return events


    def tomorrowEvents(self):
        """ get the events for the next day, from current day

        Args:
            param (class): self.

        Returns:
            (dict) events

        """
        tomorrow = ( datetime.now()+ timedelta(1)).strftime('%Y-%m-%d') 
        start = tomorrow + 'T01:01:01.951524Z'
        end = (datetime.utcnow() + timedelta(1)).isoformat() + 'Z'
        end = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')+ 'T23:59:59.951524Z'

        events = self.eventsByDate(start, end)
        return events


    def eventsByDate(self, start, end):
        """ get the events by datetime start and end

        Args:
            param (string): start. Example: 2019-01-01T23:59:59.951524Z
            param (string): end. Example: 2019-01-01T23:59:59.951524Z

        Returns:
            (dict) events

        """

        events = []

        try:
            request = self.service.events().list(calendarId='primary',
                timeMin=start, timeMax=end, singleEvents=True)

            while request != None:
              # Get the next page.
              response = request.execute()
              # Accessing the response like a dict object with an 'items' key
              # returns a list of item objects (events).
              for event in response.get('items', []):
                # The event object is a dict object with a 'summary' key.
                
                end = event.get('end')
                start = event.get('start')
                if'dateTime' in start :
                    start = parser.parse(start.get('dateTime') ).strftime('%H:%M')
                else:
                    start = "sin hora de inicio definida"
                if'dateTime' in end :
                    end = parser.parse(end.get('dateTime') ).strftime('%H:%M')
                else:
                    end = "sin hora de final definida"
                
                
                events.append({
                    "name": event.get('summary', 'NO SUMMARY'),
                    "start": start,
                    "end": end
                })

                # Get the next request object by passing the previous request object to
                # the list_next method.
                request = self.service.events().list_next(request, response)



        except AccessTokenRefreshError:
        # The AccessTokenRefreshError exception is raised if the credentials
        # have been revoked by the user or they have expired.
            print ('The credentials have been revoked or expired, please re-run'
                   'the application to re-authorize')

        return events


    def fetchEvents(self):
        """ fetch a list of events

        Returns:
            (void)

        """
      # The apiclient.discovery.build() function returns an instance of an API service
      # object can be used to make API calls. The object is constructed with
      # methods specific to the calendar API. The arguments provided are:
      #   name of the API ('calendar')
      #   version of the API you are using ('v3')
      #   authorized httplib2.Http() object that can be used for API calls

        try:

            # The Calendar API's events().list method returns paginated results, so we
            # have to execute the request in a paging loop. First, build the
            # request object. The arguments provided are:
            #   primary calendar for user
            request = self.service.events().list(calendarId='primary')
            # Loop until all pages have been processed.
            while request != None:
              # Get the next page.
              response = request.execute()
              # Accessing the response like a dict object with an 'items' key
              # returns a list of item objects (events).
              for event in response.get('items', []):
                # The event object is a dict object with a 'summary' key.
                print repr(event.get('summary', 'NO SUMMARY')) + '\n'
              # Get the next request object by passing the previous request object to
              # the list_next method.
              request = self.service.events().list_next(request, response)

        except AccessTokenRefreshError:
        # The AccessTokenRefreshError exception is raised if the credentials
        # have been revoked by the user or they have expired.
            print ('The credentials have been revoked or expired, please re-run'
               'the application to re-authorize')



# cal = GoogleCalendar()


#cal.fetchEvents()
#cal.fetchCalendars()

#cal.eventsByDate(1)
# print cal.todayEvents()

#GetCredentials()
