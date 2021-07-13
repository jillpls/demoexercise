from rest_framework import serializers
from mailing_campaign.models import ContactList, Contact
from django.contrib.auth.models import User
from mailing_campaign.mail import Campaign, Mail, MailData


class UserSerializer(serializers.ModelSerializer):
    contact_lists = serializers.PrimaryKeyRelatedField(many=True,
                                                       queryset=ContactList.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'contact_lists']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email_address"]


class ContactListSerializer(serializers.ModelSerializer):
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
    
    class Meta:
        model = ContactList
        fields = ["contacts", "id", "creation_time", "user"]


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


class CampaignSerializer(serializers.Serializer):
    video_id = serializers.IntegerField()
    template_id = serializers.IntegerField()
    contact_list_id = serializers.IntegerField()

    def create(self):
        return Campaign(**self.validated_data)


class MailDataSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    video_link = serializers.CharField()


class MailSerializer(serializers.Serializer):
    email_address = serializers.EmailField()
    data = MailDataSerializer()
    

class CampaignPostSerializer(serializers.Serializer):
    template_id = serializers.IntegerField()
    instances = MailSerializer(many=True)
