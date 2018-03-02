from django.urls import path

from core.views import PaymentView, TransactionAPI

app_name = 'payment'

urlpatterns = [
    path('', PaymentView.as_view(), name='payment-form'),
    path('transaction', TransactionAPI.as_view(), name='transaction')
]
