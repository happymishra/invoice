from django.urls import path

from apps.templateview import views

urlpatterns = [
    path('', views.UploadTemplateView.as_view())
]
