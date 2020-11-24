"""
The action package for this web system
"""
from . import web_index
from . import web_user
from . import web_sql
from . import web_monitor

web_handlers = [web_index, web_user, web_sql, web_monitor]

__all__ = 'web_handlers'

