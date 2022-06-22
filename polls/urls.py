from posixpath import basename
from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .apiviews import PollViewSet


from .apiviews import*
from .views import *

router = DefaultRouter()
router.register('polls', PollViewSet,basename='polls')

urlpatterns = [
    path("users/", UserCreate.as_view(), name="user_create"),
    path("polls/", PollList.as_view(), name="polls_list"),
    path("polls/<int:pk>/", PollDetail.as_view(), name="polls_detail"),
    path("choices/", ChoiceList.as_view(), name="choice_list"),
    path("vote/", CreateVote.as_view(), name="create_vote"),
    path("login/", LoginView.as_view(), name="login"),
    # path("login/", views.obtain_auth_token, name="login"),
]

urlpatterns += router.urls