from django.urls import path

from apps.api import views

print("Hello")
urlpatterns = [
    # path('path/', views.UploadFiles.as_view()),
    path('path/<int:pk>', views.InvoiceDetailView.as_view()),
    path('path/', views.InvoiceDetailView.as_view()),
    path('', views.HTMLView.as_view())

]

from django.conf import settings
from django.urls import include, path

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns