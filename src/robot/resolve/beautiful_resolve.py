from bs4 import BeautifulSoup

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story"> Once upon a time there were three little s isters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">< ! - Elsie ... ></a>,
    <a href="http://example.com/lacie" class="sister" id="link2"> Lacie</a> and
    <a href="http://example.com/tillie " class="sister" id="link3"> Tillie</a> ;
    and they lived at the bottom of a well .</p>
<p class="story"> ...
<p>
</body>
</html>
"""


def init():
    soup = BeautifulSoup(html, 'lxml')
    print(soup.prettify())


def node():
    soup = BeautifulSoup(html, 'lxml')
    print(soup.titile)
    print(soup.head)
    print(soup.p)


if __name__ == '__main__':
    node()
