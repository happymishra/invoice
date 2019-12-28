from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_500_INTERNAL_SERVER_ERROR,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from apps.api.invoicemanagement.models import (UploadInvoice)
from apps.api.invoicemanagement.serializers import (InvoiceUploadSerializers,
                                                    InvoiceUploadStatusSerializer)


class FileView(APIView):
    def get(self, request, upload_id):
        try:

            upload_invoice_obj = UploadInvoice.objects.get(id=upload_id)
        except UploadInvoice.DoesNotExist as ex:
            return JsonResponse({"data": {"message": "File upload id does not exists"}},
                                status=HTTP_400_BAD_REQUEST)
        except UploadInvoice.MultipleObjectsReturned as ex:
            return JsonResponse({"data": {"message": "An error occurred"}},
                                status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            serializer = InvoiceUploadStatusSerializer(upload_invoice_obj)

        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = InvoiceUploadSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def patch(self, request, upload_id):
        try:

            upload_invoice_obj = UploadInvoice.objects.get(id=upload_id)
        except UploadInvoice.DoesNotExist as ex:
            return JsonResponse({"data": {"message": "File upload id does not exists"}},
                                status=HTTP_400_BAD_REQUEST)
        except UploadInvoice.MultipleObjectsReturned as ex:
            return JsonResponse({"data": {"message": "An error occurred"}},
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = InvoiceUploadStatusSerializer(upload_invoice_obj,
                                                   data=request.data,
                                                   partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Updated status successfully"},
                                status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
