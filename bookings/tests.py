import pytest
from rest_framework.test import APIClient
from bookings.models import Room

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def room(db):
    return Room.objects.create(name="Alpha", capacity=6)

def payload(room, start, end):
    return {"room": room.id, "title": "Standup", "start": start, "end": end}

@pytest.mark.django_db
def test_create_booking(client, room):
    r = client.post("/api/bookings/", payload(room, "2026-10-12T09:00Z", "2026-10-12T10:00Z"), format="json")
    assert r.status_code == 201

@pytest.mark.django_db
def test_end_before_start_rejected(client, room):
    r = client.post("/api/bookings/", payload(room, "2026-10-12T10:00Z", "2026-10-12T09:00Z"), format="json")
    assert r.status_code == 400

@pytest.mark.django_db
def test_overlap_rejected(client, room):
    client.post("/api/bookings/", payload(room, "2026-10-12T09:00Z", "2026-10-12T10:00Z"), format="json")
    r = client.post("/api/bookings/", payload(room, "2026-10-12T09:30Z", "2026-10-12T10:30Z"), format="json")
    assert r.status_code == 400

@pytest.mark.django_db
def test_back_to_back_allowed(client, room):
    client.post("/api/bookings/", payload(room, "2026-10-12T09:00Z", "2026-10-12T10:00Z"), format="json")
    r = client.post("/api/bookings/", payload(room, "2026-10-12T10:00Z", "2026-10-12T11:00Z"), format="json")
    assert r.status_code == 201

@pytest.mark.django_db
def test_update_does_not_conflict_with_itself(client, room):
    b = client.post("/api/bookings/", payload(room, "2026-10-12T09:00Z", "2026-10-12T10:00Z"), format="json").json()
    r = client.patch(f"/api/bookings/{b['id']}/", {"title": "New"}, format="json")
    assert r.status_code == 200

@pytest.mark.django_db
def test_invalid_capacity_rejected(client):
    r = client.post("/api/rooms/", {"name": "X", "capacity": 0}, format="json")
    assert r.status_code == 400

@pytest.mark.django_db
def test_missing_fields_rejected(client):
    r = client.post("/api/bookings/", {}, format="json")
    assert r.status_code == 400