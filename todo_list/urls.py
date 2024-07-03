from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from base import views as base_views
from users import views as users_views
from tasks import views as tasks_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
