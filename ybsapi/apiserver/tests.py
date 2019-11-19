from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import User
from .serializers import UserSerializer

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_user(vk_id=''):
        if vk_id != '':
            User.objects.create(vk_id=vk_id)

    def setUp(self):
        self.create_song(1111111)
        self.create_song(2222222)
        self.create_song(3333333)
        self.create_song(4444444)

class GetAllUsersTest(BaseViewTest):

    def test_get_all_users(self):
        response = self.client.get(reverse("users"))

        expected = User.objects.all()
        serializer = UserSerializer(expected, many=True)
        print(response.data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)