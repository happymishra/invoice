from rest_framework import serializers
from rest_framework.parsers import FileUploadParser

from apps.api.invoicemanagement.models import (UploadInvoice,
                                               Address,
                                               BuyerSeller,
                                               InvoiceItem,
                                               InvoiceDetail)


class InvoiceUploadSerializers(serializers.ModelSerializer):
    parser_classes = (FileUploadParser,)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = UploadInvoice
        fields = ['id', 'user_id', 'file_path']


class InvoiceUploadStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    invoice_detail_id = serializers.IntegerField(required=False)

    class Meta:
        model = UploadInvoice
        fields = ('id', 'status', 'invoice_detail_id')

    def to_representation(self, instance):
        resp = dict()
        if instance.status == instance.DONE:
            resp['status'] = instance.get_status_display()
            resp['invoice_id'] = instance.invoice_detail_id
        else:
            resp['status'] = instance.get_status_display()

        return resp


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'pin_code']

    @staticmethod
    def update(instance, data):
        address_obj = instance.address
        for key, value in data.items():
            setattr(address_obj, key, value)
        address_obj.save()


class BuyerSellerSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = BuyerSeller
        fields = ['first_name', 'last_name', 'address']

    @staticmethod
    def create(validated_data):
        add_obj = Address.objects.create(**validated_data.pop('address'))
        buyer_seller_obj = BuyerSeller.objects.create(address=add_obj, **validated_data)
        return buyer_seller_obj

    @staticmethod
    def update(instance, buyer_seller_data, key):
        buyer_seller_obj = getattr(instance, key)

        for key, value in buyer_seller_data.items():
            if key == 'address':
                AddressSerializer.update(buyer_seller_obj, buyer_seller_data.get(key))
            else:
                setattr(buyer_seller_obj, key, value)

        buyer_seller_obj.save()


class InvoiceItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = InvoiceItem
        fields = ['id', 'name', 'quantity', 'price']

    @staticmethod
    def create(items, invoice_obj):
        invoice_items = [InvoiceItem(invoice=invoice_obj, **item)
                         for item in items]
        InvoiceItem.objects.bulk_create(invoice_items)

    @staticmethod
    def update(instance, validated_data):
        db_items = InvoiceItem.objects.filter(invoice=instance.pk)
        db_item_dict = {i.id: i for i in db_items}
        new_items = list()

        for each_item in validated_data.get('invoice_item'):
            item_id = each_item.get('id', None)
            db_item = db_item_dict.get(item_id)

            if item_id and db_item:
                for _key, _value in each_item.items():
                    setattr(db_item, _key, _value)

                db_item.save()
            else:
                invoice_obj = InvoiceItem(invoice=instance, **each_item)
                new_items.append(invoice_obj)

        if new_items:
            InvoiceItem.objects.bulk_create(new_items)


class InvoiceDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    buyer = BuyerSellerSerializer()
    seller = BuyerSellerSerializer()
    invoice_item = InvoiceItemSerializer(many=True)

    class Meta:
        model = InvoiceDetail
        fields = ['id', 'seller', 'buyer', 'amount', 'invoice_number', 'invoice_item']

    def create(self, validated_data):
        seller_obj = BuyerSellerSerializer.create(validated_data.pop('seller'))
        buyer_obj = BuyerSellerSerializer.create(validated_data.pop('buyer'))
        items = validated_data.pop('invoice_item')

        invoice_detail_obj = InvoiceDetail.objects.create(seller=seller_obj,
                                                          buyer=buyer_obj,
                                                          **validated_data)

        InvoiceItemSerializer.create(items, invoice_detail_obj)
        return invoice_detail_obj

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'invoice_item':
                InvoiceItemSerializer.update(instance, validated_data)
            elif key in ('buyer', 'seller'):
                BuyerSellerSerializer.update(instance, validated_data.get(key), key)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance
