import datetime

def get_today_date():
    """Return current date in ISO format (YYYY-MM-DD)"""
    return datetime.date.today().isoformat()

def get_now_datetime():
    """Return current date and time"""
    return datetime.datetime.now()

def get_display_date():
    """Return date formatted like 'Wednesday, 24 July 2025'"""
    d = get_now_datetime()
    return d.strftime('%A, %d %B %Y')
