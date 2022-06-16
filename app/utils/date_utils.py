def time_between_dates_in_seconds(d1, d2):
    try:
        return abs((d1 - d2).seconds)
    except TypeError:
        return -1