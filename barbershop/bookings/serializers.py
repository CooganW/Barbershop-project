from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Barber, TimeSlot, Booking


class BarberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Barber
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = User(**user_data)
        user.set_password(validated_data.pop("password"))
        user.save()

        barber = Barber.objects.create(user=user, **validated_data)
        return barber

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ["id", "barber", "day_of_week", "start_time", "end_time"]

    def validate(self, data):
        validated_data = super().validate(data)

        # Check for overlapping time slots
        if validated_data["start_time"] >= validated_data["end_time"]:
            raise serializers.ValidationError("End time must be after start time.")

        existing_slots = TimeSlot.objects.filter(
            barber=validated_data["barber"],
            day_of_week=validated_data["day_of_week"],
            start_time__lt=validated_data["end_time"],
            end_time__gt=validated_data["start_time"],
        )
        if existing_slots.exists():
            raise serializers.ValidationError(
                "Time slot overlaps with an existing slot."
            )

        return validated_data


class BookingSerializer(serializers.ModelSerializer):
    time_slot = serializers.PrimaryKeyRelatedField(queryset=TimeSlot.objects.all())

    class Meta:
        model = Booking
        fields = [
            "id",
            "time_slot",
            "customer_name",
            "customer_email",
            "customer_phone",
        ]

    def validate_time_slot(self, value):
        if value.is_booked:
            raise serializers.ValidationError("This time slot is unavailable.")
        return value

    def create(self, validated_data):
        validated_data["time_slot"].is_booked = True
        validated_data["time_slot"].save()
        return super().create(validated_data)
