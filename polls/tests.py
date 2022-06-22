from urllib import response
from django.test import TestCase
from rest_framework.test import APITestCase 
from rest_framework.test import APIRequestFactory 


# import factory
#==syntax for post request

#request = factory.post(uri, post )

from polls import apiviews

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token 
#this is the syntax
#factory = APIRequestFactory()
#request = factory.post(uri, post data)


#====rewriting the same test but now using APIclient=====
from rest_framework.test import APIClient



factory = APIRequestFactory()

class TestPoll(APITestCase):
    def setUp(self):
        # self.factory = APIRequestFactory()
        # self.view = apiviews.PollViewSet.as_view({'get':'list'})
        # self.uri = '/polls/'
        self.client = APIClient()
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User=get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',password='test'
        )

    def test_list(self):
        request = self.factory.get(self.uri,HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        request.user = self.user 

        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_list2(self):
        self.client.login(username="test", password="test")
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code ))



    #==creating anew poll by sending the question and created_by params which are needs in the POST mthd
    def test_create(self):
        self.client.login(username="test", password="test")
        params = {
            "question":"How are you","created_by":1
        }
        response =self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
# Create your tests here.
