from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED)
from rest_framework.views import APIView

from apps.api.invoicemanagement.models import (UploadInvoice)
from apps.api.invoicemanagement.serializers import (InvoiceUploadSerializers,
                                                    InvoiceUploadStatusSerializer)
from apps.api.utils.exception_handler import (BadRequestException,
                                              ValidationException,
                                              ServerException)


class FileView(APIView):
    def get(self, request, upload_id):
        try:
            upload_invoice_obj = UploadInvoice.objects.get(id=upload_id)
            serializer = InvoiceUploadStatusSerializer(upload_invoice_obj)
            return Response(serializer.data, status=HTTP_200_OK)
        except (UploadInvoice.DoesNotExist, UploadInvoice.MultipleObjectsReturned):
            raise BadRequestException("File upload id does not exists. Please enter a valid Id")
        except Exception as ex:
            raise ServerException()

    def post(self, request):
        try:
            serializer = InvoiceUploadSerializers(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
        except ValidationError:
            raise ValidationException(serializer.errors)
        except Exception as ex:
            raise ServerException()

    def patch(self, request, upload_id):
        try:

            upload_invoice_obj = UploadInvoice.objects.get(id=upload_id)

            serializer = InvoiceUploadStatusSerializer(upload_invoice_obj,
                                                       data=request.data,
                                                       partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({"message": "Updated status successfully"},
                                    status=HTTP_200_OK)
        except (UploadInvoice.DoesNotExist, UploadInvoice.MultipleObjectsReturned):
            raise BadRequestException("File upload id does not exists. Please enter a valid Id")
        except Exception as ex:
            raise ServerException()
