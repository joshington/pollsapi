from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status,viewsets
from rest_framework.response import Response

from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Poll

# Create your views here.
# In views.py
# def polls_list(request):
#     MAX_OBJECTS = 20
#     polls = Poll.objects.all()[:MAX_OBJECTS]
#     data = {"results": list(polls.values("question","created_by__username", "pub_date"))}
#     return JsonResponse(data)

# def polls_detail(request, pk):
#     poll=get_object_or_404(Poll, pk=pk)
#     data={"results":{
#         "question":poll.question,
#         "created_by":poll.created_by.username,
#         "pub_date":poll.pub_date
#     }}
#     return JsonResponse(data)

from rest_framework import generics
from rest_framework.exceptions import PermissionDenied


from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer,\
    VoteSerializer


class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDetail(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer




class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset

    def post(self,request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You cannot create choice for this poll..")
        return super().post(request, *args, **kwargs)
    


class CreateVote(APIView):
    serializer_class = VoteSerializer

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)