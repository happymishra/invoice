from django.urls import path
from apps.api import views

print("Hello")
urlpatterns = [
    path('path/', views.UploadFiles.as_view()),
    path('', views.HTMLView.as_view())
]