from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework import status
from apps.api.serializers import InvoiceUploadSerializers

class UploadFiles(APIView):
    def __int__(self):
        pass

    def post(self, request):
        # upload_id = request.GET.get('invoiceId')
        #
        # myfile = request.FILES.get('invoice')
        # fs = FileSystemStorage()
        #
        # filename = fs.save(myfile.name, myfile)
        #
        # uploaded_file_url = fs.url(filename)
        serializer = InvoiceUploadSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()

        print(serializer.errors)

        return JsonResponse({'data': "success"}, status=status.HTTP_200_OK)

    # def post(self, request):
    #


class HTMLView(APIView):
    def __int__(self):
        pass

    def get(self, request):
        return render(request, 'upload.html')
