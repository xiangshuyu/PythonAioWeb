from datetime import datetime

UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def utc_date_str_format(date_str, format_str):
    format_str = format_str if format_str else '%m%d%Y'
    return datetime.strptime(date_str, UTC_FORMAT).strftime(format_str)


def money_format(parameter_value, format_str):
    format_str = format_str if format_str else '$'
    return format_str + "{:,.2f}".format(parameter_value)


def percentage_format(parameter_value, format_str):
    return "{:.2%}".format(parameter_value)


_data_format_funcs = {
    'date': utc_date_str_format,
    'money': money_format,
    'percentage': percentage_format
}


class DateFormat(object):
    def __init__(self, data, data_type):
        self.data = data
        self.data_type = data_type

    def __format__(self, format_str):
        format_function = _data_format_funcs.get(self.data_type)
        return format_function(self.data, format_str) if format_function else self.data
