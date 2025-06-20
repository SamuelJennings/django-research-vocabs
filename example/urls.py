from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import ExampleCRUDView

User = settings.AUTH_USER_MODEL


urlpatterns = [
    *ExampleCRUDView.get_urls(),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
