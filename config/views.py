from django.shortcuts import render


def index(request):
    """Главная страница сайта"""
    context = {
        "title": "Добро пожаловать в END",
    }
    return render(request, "index.html", context)


def page_not_found(request, exception):

    return render(
        request, "includes/404.html", {"path": request.path}, status=404
    )


def server_error(request):
    return render(request, "includes/500.html", status=500)


def permission_denied(request, exception):
    return render(request, "includes/403.html", status=403)
