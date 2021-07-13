from rest_framework import serializers
from mailing_campaign.models import ContactList, Contact, Video
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    contact_lists = serializers.PrimaryKeyRelatedField(many=True, queryset=ContactList.objects.all())
    
    class Meta:
        model = User
        fields = ['id', 'username', 'contact_lists']


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email_address"]


class ContactListSerializer(serializers.Serializer):
    contacts = ContactSerializer(many=True)
    id = serializers.IntegerField(required=False)
    creation_time = serializers.DateTimeField(required=False)
    user = serializers.ReadOnlyField(source='user.username')

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        instance = ContactList.objects.create(**validated_data)
        for c in contacts_data:
            Contact.objects.create(contact_list=instance, **c)
        return instance


class ContactListSerializerGet(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)

    class Meta:
        model = ContactList
        fields = ["id", "contacts"]


class UserListsSerializer(serializers.ModelSerializer):
    contact_lists = ContactListSerializerGet(many=True)

    class Meta:
        model = User
        fields = ['contact_lists']