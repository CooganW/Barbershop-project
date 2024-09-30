from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BarberViewSet,
    TimeSlotViewSet,
    BookingViewSet,
    home,
    barber_auth,
    time_slot_manager,
    appointment_view,
)

router = DefaultRouter()
router.register(r"barbers", BarberViewSet, basename="barber")
router.register(r"time-slots", TimeSlotViewSet, basename="time-slot")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", home, name="home"),
    path("barber-auth/", barber_auth, name="barber_auth"),
    path("time-slot-manager/", time_slot_manager, name="time_slot_manager"),
    path("appointment/", appointment_view, name="appointment"),
    path("", include(router.urls)),
]
