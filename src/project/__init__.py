class A:
    def __init__(self):
        self.n = 2
        self.__a = 1

    def add(self, m):
        print('self is {0} @A.add'.format(self))
        self.n += m


class B(A):
    def __init__(self):
        super().__init__()
        self.n = 3
        self.__a = 3

    def add(self, m):
        print('self is {0} @B.add'.format(self))
        super().add(m)
        self.n += 3


# 虽然解释器会发现错误，但如果不执行到这一行就不会报错
# def test():
#    ds.count("ad")


if __name__ == '__main__':
    s = B()
    ss = 1

    print(ss == 1.0)
    if not ss:
        print(s.__dict__)
    else:
        print("--")
