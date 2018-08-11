from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth import get_user_model

from .permissions import IsOwner
from .serializers import EntrySerializer, UserSerializer
from .models import Entry


# Create your views here.
class CreateView(generics.ListCreateAPIView):
    """
    This class defines the create behaviour of our rest API
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """
        Save the POST data when creating a new entry
        """
        serializer.save(owner=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    This class handles the http GET, PUT and DELETE requests.
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class CreateUserView(generics.CreateAPIView):
    """
    Class to handle the registration of users in the API
    """
    model = get_user_model()
    permission_classes = (permissions.AllowAny)
    serializer_class = UserSerializer
