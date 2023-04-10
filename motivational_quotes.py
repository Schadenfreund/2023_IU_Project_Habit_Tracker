import requests
import json
import datetime
import os
import random

class MotivationalQuotes:
    def __init__(self):
        self.url = 'https://type.fit/api/quotes'
        self.quotes_file = 'quote_of_the_day.txt'
        self.quote = None
        self.date = None
        if os.path.isfile(self.quotes_file):
            with open(self.quotes_file, 'r') as f:
                self.quote = f.readline().strip()
                self.date = datetime.date.fromisoformat(f.readline().strip())

        if self.date != datetime.date.today():
            self.update_quote()

    def update_quote(self):
        response = requests.get(self.url)
        quotes = json.loads(response.text)
        self.quote = random.choice(quotes)['text']
        self.date = datetime.date.today()
        with open(self.quotes_file, 'w') as f:
            f.write(self.quote + '\n')
            f.write(str(self.date))

    def get_quote(self):
        if self.date != datetime.date.today():
            self.update_quote()
        return self.quote