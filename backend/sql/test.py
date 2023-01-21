import os
import time
from datetime import datetime

from sql.SqlServer import SqlServer
from sql.entities.timestamp import Timestamp


def main():
    l = []
    for _ in range(3):
        l.append(f"{datetime.now()}")
        time.sleep(2)
    print(l)


    print(sorted(l, key=lambda x: Timestamp(x)))
    print(sorted(l, key=lambda x: Timestamp(x), reverse=True))


if __name__ == '__main__':
    main()
