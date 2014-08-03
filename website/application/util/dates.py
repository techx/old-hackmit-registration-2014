from datetime import datetime

from .timezones import eastern, utc

# Declare all dates in Eastern Time and convert to UTC

utc_lottery_closing = datetime(2014, 7, 28, 11, 59, 0, 0, eastern).astimezone(utc)
