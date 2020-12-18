from lxml import etree


def html():
    htmls = etree.parse('./test.html', etree.HTMLParser())
    result = etree.tostring(htmls)
    print(result.decode('utf-8'))


def all_node():
    htmls = etree.parse('./test.html', etree.HTMLParser())
    result = htmls.xpath("//*")
    print(result)


def all_li():
    htmls = etree.parse('./test.html', etree.HTMLParser())
    li = htmls.xpath("//li")
    print(li)
    print(li[0])
    a = htmls.xpath("//li/a")  # //： 子孙 / : 子
    print(a)
    print(a[0])
    father = htmls.xpath('//a[@href="link4.html"]/../@class')  # ..： 父节点
    print(father)

    class_li = htmls.xpath('//li[@class="item-0"]')
    class_li_text = htmls.xpath('//li[@class="item-0"]/a/text()')
    print(class_li)
    print(class_li_text)


def attr():
    htmls = etree.parse('./test.html', etree.HTMLParser())
    contains = htmls.xpath('//li[contains(@class, "li")]/a/text()')
    print(contains)
    ands = htmls.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')
    print(ands)
    ors = htmls.xpath('//li[contains(@class, "li") or @name="item"]/a/text()')
    print(ors)


def order():
    htmls = etree.parse('./test.html', etree.HTMLParser())
    li1 = htmls.xpath('//div[@id="test-xpath"]//ul[@class="ul-test"]/li[1]/a/text()')
    print(li1)
    last = htmls.xpath('//li[last()]/a/text()')
    print(last)
    ranges = htmls.xpath('//li[position() < 3]/a/text()')
    print(ranges)


if __name__ == '__main__':
    order()
