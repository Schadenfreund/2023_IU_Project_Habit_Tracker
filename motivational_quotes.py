import requests
import json

class MotivationalQuotes:
    def __init__(self):
        self.url = 'https://type.fit/api/quotes'

    def get_quote(self):
        response = requests.get(self.url)
        quotes = json.loads(response.text)
        return quotes[0]['text']