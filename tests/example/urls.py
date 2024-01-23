from django.urls import path
from django.views.generic import DetailView

from .models import ExampleModel
from .views import ExampleFormView

urlpatterns = [
    path("", ExampleFormView.as_view(), name="example_form"),
    path("<pk>/", DetailView.as_view(model=ExampleModel), name="example_detail"),
]
