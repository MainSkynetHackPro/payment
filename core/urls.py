from django.urls import path

from core.views import PaymentView, process_transaction, TransactionAPI

app_name = 'payment'

urlpatterns = [
    path('', PaymentView.as_view(), name='payment-form'),
    path('transaction', TransactionAPI.as_view(), name='transaction')
]
