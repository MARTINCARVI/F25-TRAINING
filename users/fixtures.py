from users.models import User
from faker import Faker

fake = Faker()


def create_user(*, email=None, first_name=None, last_name=None):
    return User.objects.create_user(
        email=email or fake.email(),
        password="VingtCinq#1",
        is_active=True,
        first_name=first_name or fake.first_name(),
        last_name=last_name or fake.last_name(),
    )
