from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def handle(self, *args, **options):
        user_model = get_user_model()
        admin = user_model.objects.filter(email='admin@admin.com')

        if not admin.exists():
            user_model.objects.create_superuser(email='admin@admin.com',
                                                password='Vl2W3kRA',
                                                first_name='Admin',
                                                last_name='Adminovich',
                                                username='admin@admin.com')
