from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .permissions import IsOwner
from .serializers import EntrySerializer, UserSerializer, CategorySerializer, \
    ArticleSerializer
from .models import Entry, Category, Article


# Create your views here.
class CreateView(generics.ListCreateAPIView):
    """
    View to handle the creation and listing of entries.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()

    def perform_create(self, serializer):
        """
        Save the POST data when creating a new entry
        """
        serializer.save(owner=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    This class handles the management of individual entries.
    """
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class UserView(generics.ListAPIView):
    """
    View to list the users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """
    View to retrieve a user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryView(generics.ListCreateAPIView):
    """
    View to handle listing of categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """
        Save the POST data when creating a new entry
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Category.objects.filter(owner=self.request.user)
        return queryset


class CategoryDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    This class handles the http GET, PUT and DELETE requests fro categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class ArticleView(generics.ListCreateAPIView):
    """
    This class defines the create behaviour of the articles
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new article."""
        categories = Category.objects.filter(
            owner=self.request.user).filter(id=self.kwargs['pk'])
        if categories.count() == 0:
            raise PermissionDenied(
                "You do not have permission to perform this action.")
        else:
            serializer.save(owner=self.request.user, category=categories[0])

    def get_queryset(self):
        queryset = Article.objects.filter(owner=self.request.user)
        categories = Category.objects.filter(owner=self.request.user)
        if categories.count() == 0:
            raise PermissionDenied(
                "You do not have permission to perform this action.")
        else:
            category = categories.filter(id=self.kwargs['pk'])
            queryset = queryset.filter(category__in=category)
        return queryset


class ArticleDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    This class handles the http GET, PUT and DELETE requests for articles.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)
    lookup_field = 'id'
