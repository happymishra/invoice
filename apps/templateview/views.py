from django.shortcuts import render
from rest_framework.views import APIView


class UploadTemplateView(APIView):
    def get(self, request):
        return render(request, 'invoicemanagement/upload.html')
