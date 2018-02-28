import json

from decimal import *
from django.test import TestCase
from django.urls import reverse

from core.models import User

TRANSACTION_URL = reverse('payment:transaction')


class PaymentViewTest(TestCase):
    def setUp(self):
        super().setUp()
        getcontext().prec = 2

        self.user_list = []
        for i in range(1, 10):
            username = f'test{i}'
            email = f'{username}@mail.ru'
            password = username
            account = 100
            inn = i
            self.user_list.append(
                User.objects.create(username=username, email=email, password=password, account=account, inn=inn))

    def tearDown(self):
        for user in self.user_list:
            user.delete()
        self.user_list = []
        super().tearDown()

    def test_request_empty_post(self):
        response = self.client.post(TRANSACTION_URL, data=None)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': True, 'message': 'Wrong request format'}
        )

    def test_request_wrong_data(self):
        data = json.dumps({'data': 'data'})
        response = self.client.post(TRANSACTION_URL, data=data, content_type="application/json")
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': True, 'message': 'Something gone wrong'}
        )

    def test_user_not_found(self):
        data = json.dumps({'userId': '500', 'inn': '123', 'amount': '123'})
        response = self.client.post(TRANSACTION_URL, data=data, content_type="application/json")
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': True, 'message': 'User not found'}
        )

    def test_target_user_not_found(self):
        data = json.dumps({'userId': self.user_list[0].id, 'inn': '500', 'amount': '123'})
        response = self.client.post(TRANSACTION_URL, data=data, content_type="application/json")
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': True, 'message': 'Destination users not found'}
        )

    def test_not_enough_money(self):
        data = json.dumps({'userId': self.user_list[0].id, 'inn': self.user_list[1].id, 'amount': '5000'})
        response = self.client.post(TRANSACTION_URL, data=data, content_type="application/json")
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': True, 'message': 'Not enough money'}
        )

    def test_payment_success(self):
        data = json.dumps({'userId': self.user_list[0].id, 'inn': self.user_list[1].inn, 'amount': '100'})
        response = self.client.post(TRANSACTION_URL, data=data, content_type="application/json")
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': False, 'message': 'Success'}
        )

    def test_payment_one_user(self):
        user1_account = User.objects.get(id=self.user_list[0].id).account
        user2_account = User.objects.get(id=self.user_list[1].id).account

        data = json.dumps({'userId': self.user_list[0].id, 'inn': self.user_list[1].inn, 'amount': '10'})
        self.client.post(TRANSACTION_URL, data=data, content_type="application/json")

        self.assertEqual(user1_account - 10, User.objects.get(id=self.user_list[0].id).account)
        self.assertEqual(user2_account + 10, User.objects.get(id=self.user_list[1].id).account)

    def test_payment_decimal(self):
        user1_account = User.objects.get(id=self.user_list[0].id).account
        user2_account = User.objects.get(id=self.user_list[1].id).account

        data = json.dumps({'userId': self.user_list[0].id, 'inn': self.user_list[1].inn, 'amount': '10.10'})
        self.client.post(TRANSACTION_URL, data=data, content_type="application/json")

        self.assertEqual(user1_account - Decimal(10.10), User.objects.get(id=self.user_list[0].id).account)
        self.assertEqual(user2_account + Decimal(10.10), User.objects.get(id=self.user_list[1].id).account)

    def test_payment_multiple(self):
        self.user_list[1].inn = 222
        self.user_list[2].inn = 222
        self.user_list[1].save()
        self.user_list[2].save()

        user0_account = self.user_list[0].account
        user1_account = self.user_list[1].account
        user2_account = self.user_list[2].account

        amount = 10
        per_user = amount / 2

        data = json.dumps({'userId': self.user_list[0].id, 'inn': '222', 'amount': amount})
        self.client.post(TRANSACTION_URL, data=data, content_type="application/json")

        self.assertEqual(user0_account - Decimal(amount), User.objects.get(id=self.user_list[0].id).account)
        self.assertEqual(user1_account + Decimal(per_user), User.objects.get(id=self.user_list[1].id).account)
        self.assertEqual(user2_account + Decimal(per_user), User.objects.get(id=self.user_list[2].id).account)

    def test_payment_multiple_decimal(self):
        self.user_list[1].inn = 222
        self.user_list[2].inn = 222
        self.user_list[1].save()
        self.user_list[2].save()

        user0_account = self.user_list[0].account
        user1_account = self.user_list[1].account
        user2_account = self.user_list[2].account

        amount = 10.20
        per_user = amount / 2

        data = json.dumps({'userId': self.user_list[0].id, 'inn': '222', 'amount': amount})
        self.client.post(TRANSACTION_URL, data=data, content_type="application/json")

        self.assertEqual(user0_account - Decimal(amount), User.objects.get(id=self.user_list[0].id).account)
        self.assertEqual(user1_account + Decimal(per_user), User.objects.get(id=self.user_list[1].id).account)
        self.assertEqual(user2_account + Decimal(per_user), User.objects.get(id=self.user_list[2].id).account)


class TestUserManager(TestCase):
    def setUp(self):
        super().setUp()
        self.user_list = []
        for i in range(1, 10):
            username = f'test{i}'
            email = f'{username}@mail.ru'
            password = username
            account = 100
            self.user_list.append(
                User.objects.create(username=username, email=email, password=password, account=account))

    def tearDown(self):
        for user in self.user_list:
            user.delete()
        self.user_list = []
        super().tearDown()

    def test_no_inn_users(self):
        user = User.objects.get_all_with_inn()
        self.assertEqual(user.count(), 0)

    def test_inn_users_exists(self):
        self.user_list[0].inn = 1
        self.user_list[1].inn = 2

        self.user_list[0].save()
        self.user_list[1].save()

        user = User.objects.get_all_with_inn()
        self.assertEqual(user.count(), 2)

    def test_returns_correct_user(self):
        self.user_list[0].inn = 1

        self.user_list[0].save()

        user = User.objects.get_all_with_inn()
        self.assertEqual(user.count(), 1)
        self.assertEqual(user[0], self.user_list[0])
