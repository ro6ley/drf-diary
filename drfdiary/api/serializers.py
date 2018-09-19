from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import Entry, Category, Article


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


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer class to handle categories
    """
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'owner', 'date_created',
                  'date_modified')
        read_only_fields = ('date_created', 'date_modified')


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle articles
    """
    owner = serializers.ReadOnlyField(source="owner.username")
    category = serializers.ReadOnlyField(source="category.id")

    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'url', 'owner', 'category',
                  'read_status', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')
