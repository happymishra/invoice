from rest_framework import serializers
from rest_framework.parsers import FileUploadParser
from .models import UploadInvoice


class InvoiceUploadSerializers(serializers.ModelSerializer):
    parser_classes = (FileUploadParser,)

    class Meta:
        model = UploadInvoice

        fields = ['file_path']