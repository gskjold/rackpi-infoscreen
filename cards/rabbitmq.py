import requests

class CardRabbitMQ:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def lines(self):
        r = requests.get(self.url, auth=(self.username, self.password))
        return ["Message rate: {}".format(r.json())]