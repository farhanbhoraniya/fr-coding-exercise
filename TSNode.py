import time

class TransactionNode():
    def __init__(self, payer=None, points=None):
        self.payer = payer
        self.timestamp = time.time()
        self.points = points

    def __lt__(self, other):
        return self.timestamp < other.timestamp