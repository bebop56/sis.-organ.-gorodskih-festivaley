from django.urls import path

from . import views

app_name = "festivals"

urlpatterns = [
    path("", views.festivals, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:festival_id>/", views.festival_detail, name="detail"),
]
