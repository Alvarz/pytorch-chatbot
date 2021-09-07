#!/usr/bin/env python

from apiclient.discovery import build
from GoogleAPI import GetCredentials
from googlesearch import search
from oauth2client.client import AccessTokenRefreshError
"""
google search method params description
query : query string that we want to search for.
tld : tld stands for top level domain which means we want to search our result on google.com or google.in or some other domain.
lang : lang stands for language.
num : Number of results we want.
start : First result to retrieve.
stop : Last result to retrieve. Use None to keep searching forever.
pause : Lapse to wait between HTTP requests. Lapse too short may cause Google to block your IP. Keeping significant lapse will make your program slow but its safe and better option.
Return : Generator (iterator) that yields found URLs. If the stop parameter is None the iterator will loop forever.


"""



#pip install beautifulsoup4
#pip install google

class GoogleSearch:

    def __init__(self):
        """ 
        class contructor

        """
        self.authenticatedHTTP =  GetCredentials()
        self.service = build('customsearch', 'v1', http=self.authenticatedHTTP)

    def search(self, query):
        """ perform a search

        Args:
            param (class): self.
            param (str): query.

        Returns:
            void

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

            for j in search(query, tld='com.ar', lang='es', num=10, stop=1, pause=2):
                print j


        except AccessTokenRefreshError:
            # The AccessTokenRefreshError exception is raised if the credentials
            # have been revoked by the user or they have expired.
            print ('The credentials have been revoked or expired, please re-run'
               'the application to re-authorize')



#cal = GoogleSearch()

#cal.search('coco')
