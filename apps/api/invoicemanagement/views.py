from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_201_CREATED)
from rest_framework.views import APIView

from apps.api.invoicemanagement.models import (InvoiceDetail)
from apps.api.invoicemanagement.serializers import (InvoiceDetailSerializer)


class InvoiceDetailView(APIView):
    def get(self, request, invoice_id):
        try:
            query_set = InvoiceDetail.objects \
                .select_related('seller',
                                'buyer',
                                'seller__address',
                                'buyer__address') \
                .filter(id=invoice_id)

            serializer = InvoiceDetailSerializer(query_set, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as ex:
            pass

    def post(self, request):
        try:
            serializer = InvoiceDetailSerializer(data=request.data, many=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
        except Exception as ex:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        query_set = InvoiceDetail.objects \
            .select_related('seller',
                            'buyer',
                            'seller__address',
                            'buyer__address') \
            .get(id=pk)

        serializer = InvoiceDetailSerializer(query_set, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
