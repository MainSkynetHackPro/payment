from django.urls import path

from core.views import PaymentView, process_transaction

app_name = 'payment'

urlpatterns = [
    path('', PaymentView.as_view(), name='payment-form'),
    path('transaction', process_transaction, name='transaction')
]
