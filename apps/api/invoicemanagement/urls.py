from django.urls import path

from apps.api.invoicemanagement import invoice_upload_management as upload
from apps.api.invoicemanagement import views

urlpatterns = [
    path('upload/', upload.FileView.as_view()),
    path('upload/<int:upload_id>', upload.FileView.as_view()),
    path('<int:invoice_id>', views.InvoiceDetailView.as_view()),
    path('', views.InvoiceDetailView.as_view()),
]
