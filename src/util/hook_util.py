import atexit
import sys

hook_list = []

original_exit_hook = sys.exit
original_except_hook = sys.excepthook

exit_status = {}


def _custom_exit_hook(status):
    original_exit_hook(status)
    exit_status.update({"exitCode": status})
    for hook in hook_list:
        hook(exit_status)


def _custom_except_hook(exc_type, exc_obj, exc_tb):
    original_except_hook(exc_type, exc_obj, exc_tb)
    exit_status.update({"exception": exc_obj, "traceback": exc_tb, "type": exc_type})
    for hook in hook_list:
        hook(exit_status)


def add_exit_hook(hook):
    if callable(hook):
        hook_list.append(hook)

        # kwargs["exit_status"] = exit_status
        # atexit.register(hook, *args, **kwargs)
    else:
        raise AssertionError("the hook is not a callable object, please use a function or implement the __call__()")


def custom_sys_hook():
    sys.exit = _custom_exit_hook
    sys.excepthook = _custom_except_hook
