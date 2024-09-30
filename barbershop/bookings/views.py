from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Barber, TimeSlot, Booking
from .serializers import BarberSerializer, TimeSlotSerializer, BookingSerializer
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "home.html")


@login_required
def barber_auth(request):
    return render(request, "registration.html")


@login_required
def time_slot_manager(request):
    return render(request, "time_slot_manager.html")


@login_required
def appointment_view(request):
    available_timeslots = TimeSlot.objects.filter(is_booked=False)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        category = request.POST.get("category")
        chosen_timeslot = request.POST.get("chosen_timeslot")
        message = request.POST.get("message")

        # Redirect to the appointment page with the form data
        return HttpResponseRedirect(
            reverse("appointment")
            + f"?full_name={full_name}&email={email}&phone={phone}&category={category}&chosen_timeslot={chosen_timeslot}&message={message}"
        )

    return render(
        request, "appointment.html", {"available_timeslots": available_timeslots}
    )


def login(request):
    return render(request, "login.html")


class BarberViewSet(viewsets.ModelViewSet):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer
    permission_classes = [IsAuthenticated]


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(barber__user=user)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(time_slot__barber__user=user)

    def create(self, request, *args, **kwargs):
        time_slot_id = request.data.get("time_slot")
        # Check if the time slot is already booked
        if Booking.objects.filter(time_slot_id=time_slot_id).exists():
            return Response(
                {"detail": "This time slot is already booked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Proceed with creating the booking if the slot is available
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Optional: Add any additional logic like sending notifications here
        instance.delete()  # Remove the booking instance
        return Response(status=status.HTTP_204_NO_CONTENT)
