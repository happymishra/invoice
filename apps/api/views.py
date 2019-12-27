from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.models import UploadInvoice, InvoiceDetail
from apps.api.serializers import InvoiceUploadSerializers, InvoiceDetailSerializer


class UploadFiles(APIView):
    def __int__(self):
        pass

    def get(self, request):
        upload_id = request.GET.get('uploaidId')

        try:
            upload_invoice_obj = UploadInvoice.objects.get(id=upload_id)
        except UploadInvoice.DoesNotExist as ex:
            return JsonResponse({"error": "Upload Id does not exsits"},
                                status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'state': upload_invoice_obj.status},
                            status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InvoiceUploadSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print(serializer.errors)

        return Response(serializer.data, status=status.HTTP_201_OK)


class InvoiceDetailView(APIView):
    def get(self, request):
        invoice_id = request.GET.get('invoice_id')
        invoice_id = int(invoice_id)

        try:
            query_set = InvoiceDetail.objects \
                .select_related('seller',
                                'buyer',
                                'seller__address',
                                'buyer__address') \
                .filter(id=invoice_id)

            serializer = InvoiceDetailSerializer(query_set, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            pass

    def post(self, request):
        try:
            serializer = InvoiceDetailSerializer(data=request.data, many=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            # logger.error(traceback.format_exc())
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class HTMLView(APIView):
    def __int__(self):
        pass

    def get(self, request):
        return render(request, 'upload.html')
