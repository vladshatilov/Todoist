import factory.django

from core.models import Profile
from goals.models import Board, GoalCategory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    username = factory.Faker('user_name')
    password = 'test'
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True

class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker("name")


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = "Test Category Name"
    user_id = 1
    board = factory.SubFactory(BoardFactory)