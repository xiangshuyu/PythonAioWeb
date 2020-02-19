class A(object):
    def __init__(self):
        self.__a = 1

    def add(self):
        self.__a += 1


class B(A):
    def __init__(self):
        super().__init__()
        self.__a = 1

    def add(self):
        self.__a += 1


if __name__ == '__main__':
    s = B()
    s.add()
    print(s.__dict__)