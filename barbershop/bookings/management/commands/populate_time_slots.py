from django.core.management.base import BaseCommand
from bookings.models import Barber, TimeSlot
from datetime import time


class Command(BaseCommand):
    help = "Populate time slots for each barber"

    def handle(self, *args, **kwargs):
        barbers = Barber.objects.all()

        time_slots = [
            (time(10, 0), time(11, 0)),  # 24-hour format
            (time(11, 0), time(12, 0)),
            (time(13, 0), time(14, 0)),
            (time(15, 0), time(16, 0)),
            (time(16, 0), time(17, 0)),
            (time(17, 0), time(18, 0)),
        ]

        for barber in barbers:
            for day in range(3, 8):  # Wed(3) to Sun(7)
                for start_time, end_time in time_slots:
                    TimeSlot.objects.create(
                        barber=barber,
                        day_of_week=day,
                        start_time=start_time,
                        end_time=end_time,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Added time slot for {barber} on {day} from {start_time} to {end_time}"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("Time slots are full for all barbers."))
