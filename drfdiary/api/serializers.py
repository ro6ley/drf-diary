from rest_framework import serializers
from .models import Entry


class EntrySerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into the JSON format.
    """

    class Meta:
        """
        Meta class to map serializer's fields with the models fields
        """
        model = Entry
        fields = ('id', 'content', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')
