from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Entry


UserModel = get_user_model()


class EntrySerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into the JSON format.
    """
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        """
        Meta class to map serializer's fields with the models fields
        """
        model = Entry
        fields = ('id', 'content', 'owner', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle user listing
    """

    class Meta:
        model = UserModel    
        fields = ('id', 'username', 'email', 'password')
        read_only_fields = ('id', 'username', 'email')
