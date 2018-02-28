from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def get_all_with_inn(self):
        return self.exclude(inn__isnull=True)
