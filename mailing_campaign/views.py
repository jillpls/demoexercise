import requests

from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from mailing_campaign.serializers import (
    CampaignSerializer,
    CampaignPostSerializer,
    ContactListSerializer,
    UserListsSerializer,
    UserSerializer,
)
from mailing_campaign.models import ContactList, Video
from mailing_campaign.mail import CampaignPost, generate_instances


@api_view(["GET", "POST"])
def mailing_lists(request):
    """Accepts GET and POST requests for ContactLists

    Returns:
        Response: HTTP response
    """
    if request.method == "GET":
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response(request.data, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserListsSerializer(user)
        return Response(
            data=JSONRenderer().render(serializer.data), status=status.HTTP_200_OK
        )

    if request.method == "POST":
        serializer = ContactListSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
            except ValueError:
                return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=None, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def start_campaign(request):
    """Accepts POST requests to start email campaigns

    Returns:
        Response: HTTP response
    """
    if request.method != "POST":
        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(request.user, AnonymousUser):
        return Response(request.data, status=status.HTTP_401_UNAUTHORIZED)

    serializer = CampaignSerializer(data=request.data)
    if serializer.is_valid():
        campaign = serializer.create(serializer.validated_data)

        # Check if video_id exists

        try:
            video = Video.objects.filter(user=request.user).get(id=campaign.video_id)
            campaign.video = video
        except ObjectDoesNotExist:
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        # Check if mailing list exist and if it belongs to the current user

        try:
            contact_list = ContactList.objects.get(id=campaign.contact_list_id)
            campaign.contact_list = contact_list
            if contact_list.user != request.user:
                return Response(
                    data=serializer.data, status=status.HTTP_401_UNAUTHORIZED
                )
        except ObjectDoesNotExist:
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        campaign_post = CampaignPost(campaign.template_id, generate_instances(campaign))
        post_serializer = CampaignPostSerializer(campaign_post)

        request = requests.post(
            "https://jsonplaceholder.typicode.com/posts",
            data=JSONRenderer().render(post_serializer.data),
        )

    return Response(data=None, status=request.status_code)
