import time
import datetime


class A:
    def __init__(self):
        self.n = 2

    def add(self, m):
        print('self is {0} @A.add'.format(self))
        self.n += m


class B(A):
    def __init__(self):
        super().__init__()
        self.n = 3

    def add(self, m):
        print('self is {0} @B.add'.format(self))
        super().add(m)
        self.n += 3


class C(A):
    def __init__(self):
        super().__init__()
        self.n = 4

    def add(self, m):
        print('self is {0} @C.add'.format(self))
        super().add(m)
        self.n += 4


class D(B, C):
    def __init__(self):
        super().__init__()
        self.n = 5

    def add(self, m):
        print('self is {0} @D.add'.format(self))
        super().add(m)
        self.n += 5

    def tst(self, s):
        print("this is test {0}".format(s))


if __name__ == '__main__':
    print(B.mro())
    b = B()
    b.add(2)
    print(b.n)

    print("----------")
    print(D.mro())
    d = D()
    d.add(2)
    print(d.n)

    # print(D.tst(d, "ds"))
    print("date-----------")
    print(time.time())
    date = datetime.date.fromtimestamp(time.time())
    date = datetime.date.today()
    print(date)
    print(date.strftime("%Y-%m-%d"))
    print(date.strftime("%Y-%m-%d %H:%M:%S"))

    print("datetime-----------")
    dateTime = datetime.datetime.fromtimestamp(time.time())
    dateTime = datetime.datetime.now()
    print(dateTime)
    print(dateTime.strftime("%Y-%m-%d %H:%M:%S"))

    print(datetime.datetime.strptime("2019-01-22 09:22:11", "%Y-%m-%d %H:%M:%S"))
