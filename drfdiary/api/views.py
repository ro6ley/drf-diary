from django.shortcuts import render
from rest_framework import generics
from .serializers import EntrySerializer
from .models import Entry


# Create your views here.
class CreateView(generics.ListCreateAPIView):
    """
    This class defines the create behaviour of our rest API
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def perform_create(self, serializer):
        """
        Save the POST data when creating a new entry
        """
        serializer.save()
        