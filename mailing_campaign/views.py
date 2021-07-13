from rest_framework import serializers, status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mailing_campaign.serializers import ContactListSerializer, ContactListSerializerGet, UserListsSerializer, UserSerializer
from mailing_campaign.models import ContactList, Contact

from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET', 'POST'])
def mailing_lists(request):

    if request.method == 'GET':
        user = request.user
        serializer = UserListsSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_418_IM_A_TEAPOT)

    elif request.method == 'POST':
        serializer = ContactListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

