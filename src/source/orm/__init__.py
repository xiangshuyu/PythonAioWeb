class D(object):
    def __init__(self):
        super().__init__()
        self.n = 4

    def add(self, m):
        print('self is {0} @D.add'.format(self))
        self.n += 4


class E(object):
    def __init__(self):
        super().__init__()
        self.n = 5

    def add(self, m):
        print('self is {0} @E.add'.format(self))
        super().add(m)
        self.n += 5


class F(object):
    def __init__(self):
        super().__init__()
        self.n = 6

    def add(self, m):
        print('self is {0} @F.add'.format(self))
        self.n += 6


class C(D, F):
    def __init__(self):
        super().__init__()
        self.n = 3

    def add(self, m):
        print('self is {0} @C.add'.format(self))
        super().add(m)
        self.n += 3


class B(E, D):
    def __init__(self):
        super().__init__()
        self.n = 2

    def add(self, m):
        print('self is {0} @B.add'.format(self))
        super().add(m)
        self.n += 2


class A(B, C):
    def __init__(self):
        super().__init__()
        self.n = 1

    def add(self, m):
        print('self is {0} @A.add'.format(self))
        super().add(m)
        self.n += 1


if __name__ == '__main__':
    print(A.mro())
    d = A()
    d.add(2)
    print(d.n)