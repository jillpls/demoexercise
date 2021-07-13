from rest_framework import serializers
from mailing_campaign.models import ContactList, Contact, Video
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ("id", "first_name", "last_name", "email_address")


class ContactListSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)

    class Meta:
        model = ContactList
        fields = ("id", "creation_time", "contacts")

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        instance = ContactList.objects.create(**validated_data)
        for c in contacts_data:
            Contact.objects.create(contact_list=instance, **c)
        return instance