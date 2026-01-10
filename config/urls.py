from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path(
        "users/", include("users.urls", namespace="users")
    ),  # Приложение users
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "characters/", include("characters.urls", namespace="characters")
    ),  # Приложение characters
]

handler404 = "config.views.page_not_found"
handler500 = "config.views.server_error"
handler403 = "config.views.permission_denied"

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
