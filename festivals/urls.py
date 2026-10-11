from django.urls import path

from . import views

urlpatterns = [
    path("", views.festivals, name="festivals"),
    path(
        "<int:festival_id>/",
        views.festival_detail,
        name="festival_detail",
    ),
]
