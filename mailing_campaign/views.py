import requests

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
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
        if not request.user.is_authenticated:
            # Not logged in
            return Response(request.data, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserListsSerializer(user)
        # Return lists of user rendered as json
        return Response(
            data=JSONRenderer().render(serializer.data), status=status.HTTP_200_OK
        )

    if request.method == "POST":
        serializer = ContactListSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
            except ValueError:
                # User does not exist
                return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)
            # Successful post
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Invalid input
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Backup for unexpected behavior
    return Response(data=None, status=status.HTTP_40)


@api_view(["POST"])
def start_campaign(request):
    """Accepts POST requests to start email campaigns

    Returns:
        Response: HTTP response
    """

    if not request.user.is_authenticated:
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
                # This should not be reached (unless two videos share an id?)
                return Response(
                    data=serializer.data, status=status.HTTP_403_FORBIDDEN
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
