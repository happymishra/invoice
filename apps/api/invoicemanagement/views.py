"""
API view class which has all the API end points to add and update invoice
information
"""

import traceback

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_201_CREATED)
from rest_framework.views import APIView

from apps.api.invoicemanagement.models import (InvoiceDetail)
from apps.api.invoicemanagement.serializers import (InvoiceDetailSerializer)
from apps.api.utils.exception_handler import (BadRequestException,
                                              ServerException,
                                              ValidationException)
from . import logger


class InvoiceDetailView(APIView):
    """
    Contains API methods for the invoice details views
    """
    def get(self, request, invoice_id):
        try:
            query_set = InvoiceDetail.invoice_detail_objects.get(id=invoice_id)
            serializer = InvoiceDetailSerializer(query_set)
            return Response(serializer.data, status=HTTP_200_OK)
        except (InvoiceDetail.DoesNotExist, InvoiceDetail.MultipleObjectsReturned) as ex:
            raise BadRequestException("Invalid invoice id. Please enter a valid invoice id")
        except Exception as ex:
            logger.error(traceback.format_exc())
            raise ServerException()

    def post(self, request):
        try:
            serializer = InvoiceDetailSerializer(data=request.data, many=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)

        except ValidationError:
            raise ValidationException(serializer.errors)
        except Exception as ex:
            logger.error(traceback.format_exc())
            raise ServerException()

    def patch(self, request, invoice_id):
        try:
            query_set = InvoiceDetail.invoice_detail_objects.get(id=invoice_id)
            serializer = InvoiceDetailSerializer(query_set, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)

        except (InvoiceDetail.DoesNotExist, InvoiceDetail.MultipleObjectsReturned):
            raise BadRequestException("Invalid invoice id. Please enter a valid invoice id")
        except ValidationError:
            raise ValidationException(serializer.errors)
        except Exception as ex:
            logger.error(traceback.format_exc())
            raise ServerException()
