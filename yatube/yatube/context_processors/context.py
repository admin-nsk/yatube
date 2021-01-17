import datetime as dt


def year(request):
    year_now = dt.datetime.now()
    return {'year': year_now.year}
