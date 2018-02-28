import json

from decimal import Decimal
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from core.models import User


class PaymentView(TemplateView):
    template_name = 'payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['users'] = User.objects.get_all_with_inn()
        return context


@require_http_methods(["POST"])
def process_transaction(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': True, 'message': 'Wrong request format'})
    try:
        user_id = data['userId']
        target_inn = int(data['inn'])
        amount = float(data['amount'])
    except (KeyError, ValueError):
        return JsonResponse({'error': True, 'message': 'Something gone wrong'})
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': True, 'message': 'User not found'})
    target_users = User.objects.filter(inn=target_inn)
    if not target_users:
        return JsonResponse({'error': True, 'message': 'Destination users not found'})
    if amount > user.account:
        return JsonResponse({'error': True, 'message': 'Not enough money'})

    user.account -= Decimal(amount)
    user.save()

    per_user_amount = Decimal(amount/len(target_users))
    for user in target_users:
        user.account += per_user_amount
        user.save()

    return JsonResponse({'error': False, 'message': 'Success'})

