from django.urls import path
from .views import home, go, suggest, details

urlpatterns = [
    path("", home, name="home"),
    path("suggest/", suggest, name="suggest"),
    path("<slug:code>/", go, name="go"),
    path("stats/<slug:code>/", details, name="details"),
]
