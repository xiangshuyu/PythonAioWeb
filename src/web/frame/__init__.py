from .dispatcher import add_routes, add_static, add_view_resolver, response_handler, session_handler

# 在使用 from xx import * 的语法时
# __all__ 可用来限制当前 module 导出的 attr, 不在 __all__ 列表的 attr 将不会被 * 检索到
# __all__ 的元素必须是字符串
#
# 但我们仍然明确指定 attr 名来导入其它对应的 attr
# 例如: 如果将下面的session_handler去掉, * 讲不包括这个 attr, 但我们仍然可以通过 from xx import session_handler 强制导入
#
#  __all__ 是一种规范, 一般来说能够对外使用的 attr 需要定义在这里让人知道这些 attr 是可以对外使用的, 我们不应该导入不被 __all__ 包含的 attr
__all__ = ('add_routes', 'add_static', 'add_view_resolver', 'response_handler', 'session_handler')
