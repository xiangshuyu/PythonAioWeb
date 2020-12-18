from optparse import OptionParser, Values

_parser = OptionParser(version='1.0.5', add_help_option=False)

_parser.add_option("--help", action="help", help="show this help message and exit")
_parser.add_option("-h", "--host", type="string", help="the server port", default='0.0.0.0')
_parser.add_option("-p", "--port", type="int", action="append", help="the server port", default=[])
_parser.add_option("-i", "--internal", type="int", help="the thread time internal", default=200)
_parser.add_option("-d", "--data", type="string", help="the json file of database")
_parser.add_option("-t", "--template", type="string", help="the template type of system", default='jinja2')
_parser.format_help()


def init_sys_prop():
    options, args = _parser.parse_args()
    if isinstance(options, Values):
        return dict(**options.__dict__)
    else:
        return dict()


def format_sys_help():
    return _parser.format_help()


def step_duplicate_prop(prop):
    if isinstance(prop, list) and prop.__len__() > 0:
        for val in prop:
            yield val
    return None


def filter_duplicate_prop(options: dict, prop):
    ports = step_duplicate_prop(options[prop])
    try:
        next_val = next(ports)
    except StopIteration:
        next_val = None
    if next_val:
        options[prop] = next_val
    else:
        options.__delitem__(prop)
