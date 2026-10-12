from django.shortcuts import render
from rest_framework import viewsets
from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer

# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

    def get_queryset(self):
        qs = Booking.objects.all()
        room = self.request.query_params.get('room')
        if room:
            qs = qs.filter(room_id=room)
        return qs
