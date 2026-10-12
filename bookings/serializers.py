from rest_framework import serializers
from .models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity']

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Capacity must be a positive integer.")
        return value

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'title', 'start', 'end', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        start = data.get('start', getattr(self.instance, 'start', None))
        end = data.get('end', getattr(self.instance, 'end', None))
        room = data.get('room', getattr(self.instance, 'room', None))

        if end <= start:
            raise serializers.ValidationError("End must be after start.")

        overlapping = Booking.objects.filter(room=room, start__lt=end, end__gt=start)
        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)
        if overlapping.exists():
            raise serializers.ValidationError("This booking overlaps with an existing booking.")
        return data