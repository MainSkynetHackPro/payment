from decimal import Decimal
from rest_framework import serializers

from core.models import User


class TransactionSerializer(serializers.Serializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=User.objects.get_all_with_inn(),
                                                error_messages={'does_not_exist': 'User not found'})
    inn = serializers.IntegerField()
    amount = serializers.DecimalField(decimal_places=2, max_digits=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_users = None

    def is_valid(self, raise_exception=False):
        valid = super().is_valid(raise_exception=raise_exception)
        if valid:
            self.current_user = self.validated_data['userId']
            if Decimal(self.data['amount']) > self.current_user.account:
                self._errors['amount'] = "Not enough money"
                return False
        return valid

    def validate_inn(self, inn):
        users = User.objects.filter(inn=inn)
        if not users:
            raise serializers.ValidationError("Users not found")
        self.target_users = users
        return inn

    def save(self, **kwargs):
        self.current_user.account -= self.validated_data['amount']
        self.current_user.save()

        per_user_amount = Decimal(self.validated_data['amount'] / len(self.target_users))
        for user in self.target_users:
            user.account += per_user_amount
            user.save()
