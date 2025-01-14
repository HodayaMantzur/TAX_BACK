from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import UserSerializer
from .models import Client, Transaction
from .serializers import ClientSerializer, TransactionSerializer, CreateUserSerializer
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User as DjangoUser
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from django.db.models import Sum


# ------------------------ דף הבית ------------------------

def home(request):
    """ דף הבית עם קישורים לכניסת משתמש ואדמין """
    return render(request, 'home.html')

# ------------------------ התחברות ------------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """ יצירת יוזר חדש והחזרת טוקן """
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User created successfully!",
            "user": serializer.data,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def user_login(request):
    """ התחברות משתמש רגיל """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        login(request, user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username
        }, status=200)
    return Response({'error': 'Invalid credentials'}, status=401)

# ------------------------ ניהול חשבוניות ------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def invoice_list(request):
    """ רשימת חשבוניות של המשתמש המחובר """
    transactions = Transaction.objects.filter(user=request.user)  # סינון לפי המשתמש המחובר
    serializer = TransactionSerializer(transactions, many=True)
    return Response({'transactions': serializer.data}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invoice_create(request):
    """ יצירת חשבונית חדשה """
    data = request.data
    
    # חישוב הסכום הכולל (amount * quantity)
    try:
        quantity = int(data.get('quantity', 1))  # ברירת מחדל כמות 1
        amount_per_unit = float(data.get('amount', 0))  # ברירת מחדל מחיר 0
        total_amount = quantity * amount_per_unit
        data['amount'] = total_amount
    except ValueError:
        return Response({'errors': 'Invalid quantity or amount'}, status=400)
    
    serializer = TransactionSerializer(data=data)
    if serializer.is_valid():
        transaction = serializer.save(user=request.user)
        print(f"Saved transaction: {transaction}")  # בדיקת הנתונים שנשמרו
        return Response({'message': 'Invoice created successfully', 'transaction': serializer.data}, status=201)
    else:
        # הדפסת השגיאות ללוג ובחזרה ללקוח
        print(serializer.errors)
        return Response({'errors': serializer.errors}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    """ החזרת פרטי המשתמש המחובר """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# ------------------------ ניהול לקוחות ------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def client_list_create(request):
    """ הצגת רשימת לקוחות ויצירת לקוח חדש """
    if request.method == 'GET':
        clients = Client.objects.filter(user=request.user)  # סינון לפי המשתמש המחובר
        serializer = ClientSerializer(clients, many=True)
        return Response({'clients': serializer.data}, status=200)
    elif request.method == 'POST':
        data = request.data
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            client = serializer.save(user=request.user)
            return Response({'message': 'Client created successfully', 'client': serializer.data}, status=201)
        return Response({'errors': serializer.errors}, status=400)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def client_update_delete(request, pk):
    """ עדכון או מחיקה של לקוח """
    client = get_object_or_404(Client, pk=pk, user=request.user)
    if request.method == 'PUT':
        data = request.data
        serializer = ClientSerializer(client, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Client updated successfully', 'client': serializer.data}, status=200)
        return Response({'errors': serializer.errors}, status=400)
    elif request.method == 'DELETE':
        client.delete()
        return Response({'message': 'Client deleted successfully'}, status=200)

# ------------------------ דפי ניהול ------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    """ דף ניהול המנהל - הצגת כל המשתמשים """
    print(f"User: {request.user}, Is admin: {getattr(request.user, 'is_admin', False)}")

    if request.user.is_admin:
        users = User.objects.all()
        return Response({'users': [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]}, status=200)
    return Response({'error': 'Unauthorized'}, status=403)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_dashboard(request):
    """ דף ניהול יוזר - רשימת לקוחות וחשבוניות """
    clients = Client.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    total_amount = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    client_serializer = ClientSerializer(clients, many=True)
    transaction_serializer = TransactionSerializer(transactions, many=True)
    return Response({
        'clients': client_serializer.data,
        'transactions': transaction_serializer.data,
        'total_amount': total_amount,
    }, status=200)


