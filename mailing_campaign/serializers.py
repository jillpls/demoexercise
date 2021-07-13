from rest_framework import serializers
from mailing_campaign.models import ContactList, Contact, Video
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class ContactSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email_address = serializers.CharField()

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email_address = validated_data.get('email_address')
        return instance

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)


class ContactListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.ReadOnlyField(source='user.username')
    contacts = ContactSerializer(many=True)

    def update(self, instance, validated_data):
        instance.contacts = validated_data.get('contacts')
        return instance

    def create(self, validated_data):
        contact_list = ContactList.objects.create(**validated_data)
        return contact_list
