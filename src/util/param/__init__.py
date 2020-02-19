import inspect


def f0(a, b, c):
    print('a =', a, 'b =', b, 'c =', c)


def f1(a, b, c=0, *d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)


def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)


def f3(a, b, c=0, *d, e, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'e = ', e, 'kw =', kw)


if __name__ == '__main__':
    params = inspect.signature(f3).parameters
    for name, param in params.items():
        print('-----------')
        print(name)
        print(param.kind)
    del f3
