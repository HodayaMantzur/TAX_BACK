from multiprocessing.connection import Client
from django import forms
from users import serializers
from users.models import User
from .models import Transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import User
from .models import Transaction, Client

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # הוספת שם המשתמש ל-token
        token['username'] = user.username
        token['first_name'] = user.first_name  # הוספת השם הפרטי
        # ניתן להוסיף כאן עוד מידע שתרצה להחזיר בתוך ה-token
        
        return token



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # fields = ['amount', 'date', 'category', 'description', 'attachment']
        fields = ['type', 'amount', 'date', 'category', 'description', 'client', 'invoice_file']  # ללא 'user'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        # fields = ['name', 'email', 'phone', 'address']
