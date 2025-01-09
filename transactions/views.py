from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from rest_framework.response import Response
from users.models import User
from .models import Transaction, Client
from .serializers import TransactionForm, ClientForm
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from transactions.models import Transaction  # ודא שמסלול המודל נכון

@api_view(['POST', 'GET'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)  # שימוש בפונקציה מאובטחת
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # טיפול בבקשת GET
    return Response({'error': 'Login requires POST method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # אימות באמצעות JWT
def invoice_list(request):
    user = request.user  # המשתמש מאומת דרך הטוקן
    transactions = Transaction.objects.filter(user=user, type='income')
    transactions_data = [
        {
            'id': transaction.id,
            'amount': transaction.amount,
            'date': transaction.date.strftime('%Y-%m-%d'),
            'category': transaction.category.name if transaction.category else None,
            'description': transaction.description,
            'attachment': transaction.attachment.url if transaction.attachment else None,
        }
        for transaction in transactions
    ]
    return Response({'transactions': transactions_data}, status=200)

@csrf_exempt
def client_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = ClientForm(data)
            if form.is_valid():
                client = form.save(commit=False)
                client.user = request.user
                client.save()
                return JsonResponse({
                    'message': 'Client created successfully',
                    'client': {
                        'id': client.id,
                        'name': client.name,
                        'email': client.email,
                        'phone_number': client.phone_number, 
                        'address': client.address,
                    }
                }, status=201)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)  # הסרנו את user=request.user אם לא נחוץ
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = ClientForm(data, instance=client)
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'message': 'Client updated successfully',
                    'client': {
                        'id': client.id,
                        'name': client.name,
                        'email': client.email,
                        'phone': client.phone,
                        'address': client.address,
                    }
                }, status=200)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)  # הסרנו את user=request.user אם לא נחוץ
    if request.method == 'DELETE':
        client.delete()
        return JsonResponse({'message': 'Client deleted successfully'}, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def client_list(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        clients_data = [
            {
                'id': client.id,
                'name': client.name,
                'email': client.email,
                'phone_number': client.phone_number,
                'address': client.address,
            }
            for client in clients
        ]
        return JsonResponse({'clients': clients_data}, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def invoice_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # יצירת הטופס ללא user, ואז הוספת user לנתוני המודל
            form = TransactionForm(data)
            if form.is_valid():
                transaction = form.save(commit=False)  # עדיין לא נשמר
              #  transaction.user = print(request.user)  # הוספת המשתמש המחובר
                transaction.user = request.user
                transaction.type = ""  # ערך חוקי מתוך TYPE_CHOICES
                transaction.save()
                return JsonResponse({
                    'message': 'Invoice created successfully',
                    'transaction': {
                        'id': transaction.id,
                        'amount': transaction.amount,
                        'date': transaction.date.strftime('%Y-%m-%d'),
                        'category': transaction.category.name if transaction.category else None,
                        'description': transaction.description,
                    }
                }, status=201)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
