from rest_framework import serializers

from users.models import User
from .models import Client, Transaction

class ClientSerializer(serializers.ModelSerializer):
    """ סיריאליזר לניהול לקוחות """
    class Meta:
        model = Client
        fields = ['id', 'name', 'id_number', 'email', 'phone_number', 'address', 'notes', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    """ סיריאליזר לניהול חשבוניות """
    category_name = serializers.ReadOnlyField(source='category.name')  # להציג את שם הקטגוריה במקום ID
    client_name = serializers.ReadOnlyField(source='client.name', default='No Client')  # ערך ברירת מחדל

    class Meta:
        model = Transaction
        fields = [
            'id',
            'type',
            'amount',
            'quantity',  # שדה כמות
            'include_vat',  # שדה מע"מ
            'date',
            'category',
            'category_name',
            'description',
            'client',
            'client_name',
            'invoice_file',
            'created_at',
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user