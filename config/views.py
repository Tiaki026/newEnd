from django.shortcuts import render


def index(request):
    """Главная страница сайта."""
    context = {
        "title": "Добро пожаловать в END",
    }
    return render(request, "index.html", context)


def page_not_found(request, exception):
    """404."""
    context = {
        "title": "Страница не найдена | END",
        "path": request.path,
    }
    return render(request, "includes/404.html", context, status=404)


def server_error(request):
    """500."""
    context = {
        "title": "Ошибка сервера | END",
    }
    return render(request, "includes/500.html", context, status=500)


def permission_denied(request, exception):
    """403."""
    context = {
        "title": "Доступ запрещен | END",
    }
    return render(request, "includes/403.html", context, status=403)


def csrf_failure(request, reason=""):
    """CSRF 403."""
    context = {
        "title": "Ошибка безопасности | END",
    }
    return render(request, "includes/403csrf.html", context)
