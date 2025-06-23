from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin2@admin.ru",
            first_name="Admin",
            last_name="User",
            is_staff=True,
            is_superuser=True,
            user_role="Администратор"
        )

        user.set_password("admin")
        user.save()
