import json

from decimal import Decimal
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
from core.serializers import TransactionSerializer


class PaymentView(TemplateView):
    template_name = 'payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['users'] = User.objects.get_all_with_inn()
        return context


class TransactionAPI(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'error': False})
        return Response({'error': serializer.errors})
