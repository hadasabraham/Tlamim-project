from dateutil.parser import parse


class Timestamp(object):

    def __init__(self, timestamp: str):
        self.timestamp = timestamp

    def __le__(self, other):
        t1 = parse(self.timestamp)
        t2 = parse(other.timestamp)
        return t1 <= t2

    def __lt__(self, other):
        t1 = parse(self.timestamp)
        t2 = parse(other.timestamp)
        return t1 < t2


    def __gt__(self, other):
        t1 = parse(self.timestamp)
        t2 = parse(other.timestamp)
        return t1 > t2

    def __ge__(self, other):
        t1 = parse(self.timestamp)
        t2 = parse(other.timestamp)
        return t1 >= t2

