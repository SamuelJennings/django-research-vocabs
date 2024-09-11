from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import ExampleCRUDView

urlpatterns = [
    *ExampleCRUDView.get_urls(),
    path("vocabularies/", include("research_vocabs.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
