from django.urls import reverse
from faker import Faker
from freezegun import freeze_time
from rest_framework.test import APITestCase

from tests.factories import UserFactory


def test_init():
    assert True


def test_root_not_found(client):
    response = client.get("/")
    assert response.status_code == 404


class BaseAPITest(APITestCase):
    def setUp(self):
        self._faker = Faker()
        self._password = self._faker.password()
        self.user = UserFactory.create()
        self.user.set_password(self._password)
        self.user.save()


class LoginTest(BaseAPITest):
    url = reverse('core:login')

    @freeze_time('2022-01-01T01:00:00')
    def test_success_login(self):
        assert self.user.last_login is None