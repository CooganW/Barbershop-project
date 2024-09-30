from django.db import models
from django.contrib.auth.models import User


class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"


class TimeSlot(models.Model):
    DAYS_OF_WEEK = [
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, default=3)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = (("barber", "day_of_week", "start_time"),)

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time} - {self.end_time}"


class Booking(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="confirmed"
    )

    def __str__(self):
        return f"Booking for {self.customer_name} at {self.time_slot.start_time} - Status: {self.status}"
