from rest_framework import serializers
from ..models import Event, EventGuest

class EventGuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventGuest
        fields = ('id', 'event', 'guest', 'status',)


class EventSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format="%Y-%m-%d", source='date')
    # guests = EventGuestSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'guests', 'start', 'location', 'color',)

    def get_alternate_name(self, obj):
        return obj.alternate_name
