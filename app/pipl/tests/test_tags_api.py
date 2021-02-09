from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.gis.geos import Point


from core.models import Tag

from pipl.serializers import TagSerializer

TAGS_URL = reverse('pipl:tag-list')

class PublicTagsApiTestCase(TestCase):
    """ Test the publicly available tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags""" 
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTestCase(TestCase):
    """ Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'nick@gmail.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """ Test retrieving tags"""
        Tag.objects.create(user=self.user, name="likes_clubbing", location=Point(6.443788, 3.525202))
        Tag.objects.create(user=self.user, name="likes_chinese", location=Point(6.45390, 3.51290))

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@email.com'
            'testpass'
        )
        Tag.objects.create(user=user2, name="likes_kayaking", location=Point(6.42110, 3.34559))
        tag = Tag.objects.create(user=self.user, name="likes_chinese", location=Point(6.45390, 3.51290))

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
