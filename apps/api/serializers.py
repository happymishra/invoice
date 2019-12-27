from rest_framework import serializers
from rest_framework.parsers import FileUploadParser

from .models import UploadInvoice, Address, BuyerSeller, InvoiceItem, InvoiceDetail


class InvoiceUploadSerializers(serializers.ModelSerializer):
    parser_classes = (FileUploadParser,)

    class Meta:
        model = UploadInvoice
        fields = ['user_id', 'file_path']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'pin_code']


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


class InvoiceItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = InvoiceItem
        fields = ['id', 'name', 'quantity', 'price']


class InvoiceDetailSerializer(serializers.ModelSerializer):
    buyer = BuyerSellerSerializer()
    seller = BuyerSellerSerializer()
    invoice_item = InvoiceItemSerializer(many=True)

    class Meta:
        model = InvoiceDetail
        fields = ['seller', 'buyer', 'amount', 'invoice_number', 'invoice_item']

    def create(self, validated_data):
        seller_obj = BuyerSellerSerializer.create(validated_data.pop('seller'))
        buyer_obj = BuyerSellerSerializer.create(validated_data.pop('buyer'))
        items = validated_data.pop('invoice_item')

        invoice_detail_obj = InvoiceDetail.objects.create(seller=seller_obj,
                                                          buyer=buyer_obj,
                                                          **validated_data)

        invoice_items = [InvoiceItem(invoice=invoice_detail_obj, **item)
                         for item in items]
        InvoiceItem.objects.bulk_create(invoice_items)
        return invoice_detail_obj

        print("Hello")

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'invoice_item':
                db_item = InvoiceItem.objects.filter(invoice=instance.pk)
                db_item_dict = {i.id: i for i in db_item}
                item = validated_data.get('invoice_item')

                for each_item in item:
                    item_id = each_item.get('id', None)
                    db_item = db_item_dict.get(item_id)
                    if item_id and db_item:
                        for _key, _value in each_item.items():
                            setattr(db_item, _key, _value)

                        db_item.save()
                    else:
                        InvoiceItem.objects.create(invoice=instance, **each_item)
            elif key in ('buyer', 'seller'):
                buyer_seller_obj = getattr(instance, key)

                for _key, _value in value.items():
                    if _key == 'address':
                        addr_obj = buyer_seller_obj.address
                        for a, b in _value.items():
                            setattr(addr_obj, a, b)
                        addr_obj.save()
                    else:
                        setattr(buyer_seller_obj, _key, _value)
                buyer_seller_obj.save()
            else:
                setattr(instance, key, value)

        instance.save()

        return instance
