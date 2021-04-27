import time

class TransactionNode():
    def __init__(self, payer=None, points=None, timestamp=None):
        self.payer = payer
        self.timestamp = timestamp
        self.points = points

    def __lt__(self, other):
        return self.timestamp < other.timestamp