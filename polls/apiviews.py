from rest_framework.views import APIView
from rest_framework import generics,status,viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate

from .models import Poll, Choice
from  .serializers import*

from rest_framework.exceptions import PermissionDenied

class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username,password=password)

        if user:
            return Response({"token":user.auth_token.key})
        else:
            return Response({"error":"Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    # def destroy(self, request, *args, **kwargs):
    #     poll = Poll.objects.get(pk=self.kwargs["pk"])
    #     if not request.user == poll.created_by:
    #         raise PermissionDenied("You can not delete this poll")
    #     raise super().destroy(request, *args, **kwargs)



class PollList(APIView):
    def get(self, request):
        polls = Poll.objects.all()[:20]
        data = PollSerializer(polls, many=True).data
        return Response(data)


class PollDetail(APIView):
    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        data = PollSerializer(poll).data
        return Response(data)