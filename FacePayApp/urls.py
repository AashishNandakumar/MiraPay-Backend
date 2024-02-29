from django.urls import path
from . import views

urlpatterns = [
    path("add-data/", views.AddData.as_view()),  # add user info + financial info into the DB (POST)
    path("generate-uuid/", views.GenerateUUID.as_view()),  # generate uuid which acts as the primary key (GET)
    path("generate-signed-url/", views.GenerateSignedURLs.as_view())  # generate signed urls (GET)
]
