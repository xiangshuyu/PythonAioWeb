from pyquery import PyQuery as pq

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <div id="container">
        <ul class="list">
            <li class="li item-0"><a href="link1.html">first item</a></li>
            <li class="item-1 li" name="item"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html">third item</a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
</body>
</html>
"""


def base():
    doc = pq(html)
    print(doc('li'))


def from_url():
    doc = pq(url="https://www.taobao.com")
    print(doc('title'))


def from_file():
    doc = pq(filename="./test.html")
    print(doc('li'))


def base_select():
    doc = pq(html)
    print(doc('#container .list li'))
    print(type(doc('#container .list li')))


def find():
    doc = pq(html)
    lists = doc('.list')
    find_li = lists.children('li')
    find_a = lists.find('a')
    find_p = lists.parent()
    find_ps = lists.parents()
    print("======== find: ")
    print(find_a)
    print("======== children: ")
    print(find_li)
    print("======== parent: ")
    print(find_p)
    print("======== parents: ")
    print(find_ps)


def attr():
    doc = pq(html)
    a = doc('.item-0.active a')
    print(a)
    print(a.attr('href'))
    print(a.text())


if __name__ == '__main__':
    attr()
