import datetime


def current_year(request):
    """Добавляет текущий год в контекст шаблонов"""
    today = int(datetime.datetime.now().year)
    return {
        "year": today,
    }
