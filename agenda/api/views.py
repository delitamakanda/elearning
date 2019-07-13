from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..models import Event
from .serializers import EventSerializer

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)
