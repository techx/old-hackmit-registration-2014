from .timezones import utc, eastern

def format_utc_datetime(utc_datetime, local_timezone):
    local_datetime = utc_datetime.replace(tzinfo=utc).astimezone(local_timezone)
    return "{month} {d.day}, {hour}:{minute} {half} {tzname}".format(d=local_datetime, month=local_datetime.strftime('%B'), hour=local_datetime.strftime('%I').lstrip('0'), minute=local_datetime.strftime('%M'), half=local_datetime.strftime('%p'), tzname=local_datetime.tzname())

