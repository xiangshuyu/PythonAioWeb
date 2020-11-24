from functools import wraps
from src.util.logger.logger import logger_info
from src.util.logger.logger import logger_error


# 使用Flask定义URL的时候，如果出现
# "AssertionError: View function mapping is overwriting an existing endpoint function"这个异常信息，
# 就说明定义了多个同名的视图函数，只需要改成不同的函数名即可。
#
# 这是因为flask中url跟视图函数并不是直接对应的，而是有一个中间者-endpoint。
# 三者之间的关系是这样的：
# url---->endpoint---->view_function
#
# 它们是一对一的关系，在注册add_url_rule的时候，如果不指定endpoint，
# 那么endpoint就会默认为函数名字(__name__)，如果同一个endpoint于多个url注册的话，
# 就会发生冲突，从而抛出异常。

def logger(func):
    """
        在Python 2.5中 functools模块被引入。
        它包含了 functools.wraps()函数，这个函数会将被装饰函数的名称、模块、文档字符串拷贝到封装函数
        标注此装饰器以覆盖封装函数的__name__，避免上述报错
        :param func: controller函数
        :return: 封装函数
    """
    logger_info.debug("log proxy method : %s", func.__name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        rsp = None
        try:
            pre_handler(func)
            rsp = func(*args, **kwargs)
            post_handler(func)
        except Exception as e:
            execpt_handler(e)
        return rsp

    return wrapper


def pre_handler(func):
    logger_info.info("handler pre: %s" % func.__name__)


def post_handler(func):
    logger_info.info("handler post: %s" % func.__name__)


def execpt_handler(e):
    logger_error.error("handler request error : %s" % e)
    logger_error.exception(e)
