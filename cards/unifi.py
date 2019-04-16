from pymongo import MongoClient

class CardUnifi:
    def __init__(self):
        self.mcli = MongoClient('localhost', 27117)
        self.mdb = self.mcli.ace_stat
        self.mcol = self.mdb.stat_5minutes

    def lines(self):
        return {"Clients: :d".format(self.mcol.find_one({"o":"site"}, sort=[("time", pymongo.DESCENDING)]))}
