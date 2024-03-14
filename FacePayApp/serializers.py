from rest_framework import serializers
from . import models


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


class InvoiceInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InvoiceInformation
        fields = "__all__"
