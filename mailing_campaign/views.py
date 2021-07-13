from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mailing_campaign.serializers import ContactListSerializer


@api_view(['GET', 'POST'])
def mailing_lists(request):

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        serializer = ContactListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

