
from datetime import datetime
#from naturalLang.WordProcess import WordProcess
#from google.GoogleCalendar import GoogleCalendar
#from google.GoogleSearch import GoogleSearch
import random

# pip install numpy==1.11.0


# pip install sklearn
# import nltk
# nltk.download('averaged_perceptron_tagger')
# nltk.download('cess_esp')

# pip install --upgrade google-api-python-client

class Actions:

    def __init__(self):
        """ 
        class contructor

        """

        #self.googleSearch = GoogleSearch()
        #self.googleCalendar = GoogleCalendar()
        #self.wordProcess = WordProcess()

        self.dayWeek = {
            "Sunday": "Domingo",
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miercoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sabado",
        }
        # self.wordProcess.loadModel()

    def dispatchAction(self, action, response, sentence=None, patterns=None,
                       responsesList=None):
        """ Select the action to be permormed.

        Args:
            param (str): action.
            param (str): response.
            param (str): sentence.
            param (str): pattern.

        Returns:
            str

        """

        if action == "gettime":
            return self._getTime(response)
        if action == "getdate":
            return self._getDate(response)
        if action == "getday":
            return self._getDay(response)
        if action == "search":
            return self._search(response, sentence)
        if action == "todayevents":
            return self._todayEvents(responsesList)
        if action == "tomorrowevents":
            return self._tomorrowEvents(responsesList)

    def _getTime(self, response):
        """ get the current time

        Args:
            param (str): response.

        Returns:
            str

        """

        time = datetime.now().strftime('%H:%M:%S')
        return response.replace("{{time}}", time)

    def _getDay(self, response):
        """ get the current day name

        Args:
            param (str): response.

        Returns:
            str

        """

        day = datetime.now().strftime('%A')
        parsedDay = self.dayWeek[day] if self.dayWeek[day] is not None else day
        return response.replace("{{day}}", parsedDay)

    def _getDate(self, response):
        """ get the current date

        Args:
            param (str): response.

        Returns:
            str

        """
        date = datetime.now().strftime('%Y-%m-%d')
        return response.replace("{{date}}", date)

    def _tomorrowEvents(self, responses):
        # events = self.googleCalendar.tomorrowEvents()

        # for event in events:
        #     response = random.choice(responses)
        #     response = response.replace("{{name}}", event['name'])
        #     response = response.replace("{{start}}", event['start'])
        #     response = response.replace("{{end}}", event['end'])
        #     print(response)
        return 'alguna otra pregunta?'

    def _todayEvents(self, responses):
        #events = self.googleCalendar.todayEvents()

        # for event in events:
        # response = random.choice(responses)
        # response = response.replace("{{name}}", event['name'])
        # response = response.replace("{{start}}", event['start'])
        # response = response.replace("{{end}}", event['end'])
        # print(response)

        # for event in len(events):

        return 'alguna otra pregunta?'

    def _search(self, response, sentence):
        """ perform a search

        Args:
            param (str): response.
            param (str): sentence.

        Returns:
            str

        """

        # tag the sentence
        #tagged = self.wordProcess.cleanAndTagSentence(sentence)
        # build the query to be used
        #question = self.wordProcess.buildRealQuery(tagged)
        #response = self.googleSearch.search(question)

        # print response

        # return question
