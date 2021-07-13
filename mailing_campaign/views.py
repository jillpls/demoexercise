from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mailing_campaign.serializers import CampaignSerializer, ContactListSerializer, UserListsSerializer, UserSerializer
from mailing_campaign.models import ContactList, Video

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


@api_view(['GET', 'POST'])
def start_campaign(request):

    if request.method != 'POST':
        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

    serializer = CampaignSerializer(data=request.data)
    if serializer.is_valid():
        campaign = serializer.create()
        
        # Check if video_id exists
        
        try: 
            x : int = campaign.video_id
            video = Video.objects.filter(user=request.user).get(id=x)
            print(video)
        except ObjectDoesNotExist:
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if mailing list exist and if it belongs to the current user

        try:
            contact_list = ContactList.objects.get(id=campaign.contact_list_id)
            if contact_list.user != request.user:
                return Response(data=serializer.data, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)
        



    return Response(data=None, status=status.HTTP_404_NOT_FOUND)