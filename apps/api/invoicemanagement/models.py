"""
Contains all the models of the invoicemanagement app
"""

from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import InvoiceDetailManager
from .utils import get_file_path


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)

    class Meta:
        db_table = "address"


class BuyerSeller(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        db_table = "buyerseller"


class InvoiceDetail(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=20, null=True)
    seller = models.ForeignKey(BuyerSeller, on_delete=models.SET_NULL,
                               null=True, related_name='seller')
    buyer = models.ForeignKey(BuyerSeller, on_delete=models.SET_NULL,
                              null=True, related_name='buyer')
    invoice_date = models.DateTimeField(null=True)
    amount = models.FloatField(null=True)

    objects = models.Manager()
    invoice_detail_objects = InvoiceDetailManager()

    class Meta:
        db_table = "invoicedetail"


class UploadInvoice(models.Model):
    NEW = 0
    IN_PROGRESS = 1
    DONE = 2

    StatusChoices = (
        (NEW, _("New")),
        (IN_PROGRESS, _("InProgress")),
        (DONE, _("Done")),
    )

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=11)
    status = models.IntegerField(choices=StatusChoices, default=NEW)
    creation_date = models.DateTimeField(default=datetime.now)
    file_path = models.FileField(upload_to=get_file_path)
    invoice_detail = models.ForeignKey(InvoiceDetail, on_delete=models.CASCADE,
                                       null=True)

    class Meta:
        db_table = "uploadinvoice"


class InvoiceItem(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(InvoiceDetail,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='invoice_item')
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        db_table = "item"
