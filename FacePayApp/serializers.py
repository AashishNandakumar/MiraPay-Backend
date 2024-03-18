from rest_framework import serializers
from . import models


# User Information Serializers
# Serialize Financial Information
class FinancialInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FinancialInformation
        fields = "__all__"


# serialize User Information
class UserInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserInformation
        fields = "__all__"


# Invoice Serializers
class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Item
        fields = ['name', 'quantity', 'price', 'description', 'category']


class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = models.Invoice
        fields = ['invoice_number', 'due_date', 'from_name', 'from_email_address', 'from_phone_number', 'to_name', 'to_email_address', 'to_phone_number', 'discount_percentage', 'tax_percentage', 'total_cost', 'notes', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = models.Invoice.objects.create(**validated_data)

        for item_data in items_data:
            models.Item.objects.create(invoice=invoice, **item_data)

        return invoice
