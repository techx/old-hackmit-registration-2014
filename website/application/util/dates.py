from functools import wraps

from flask import abort

from datetime import datetime

from .timezones import eastern, utc

# Declare all dates in Eastern Time and convert to UTC

dates = {}
dates['lottery_closing'] = datetime(2014, 7, 28, 23, 59, 59, 999999, eastern).astimezone(utc)

def has_passed(test_datetime):
    if isinstance(test_datetime, str):
        test_datetime = dates[test_datetime]
    return datetime.utcnow().replace(tzinfo=utc) > test_datetime.astimezone(utc)

def get_passed_dates():
    passed_dates = {}
    for utc_datetime in dates:
        if has_passed(dates[utc_datetime]):
            passed_dates[utc_datetime] = dates[utc_datetime]
    return passed_dates

def before(test_datetime):
    def wrap(view_func):
        @wraps(view_func)
        def wrapped_timed_function(*args, **kwargs):
            if has_passed(test_datetime):
                abort(404)
            return view_func(*args, **kwargs)
        return wrapped_timed_function
    return wrap

def after(test_datetime):
    def wrap(view_func):
        @wraps(view_func)
        def wrapped_timed_function(*args, **kwargs):
            if not has_passed(test_datetime):
                abort(404)
            return view_func(*args, **kwargs)
        return wrapped_timed_function
    return wrap
