# Generated by Django 5.1.1 on 2024-09-28 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0010_customuser"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customuser",
            old_name="phone_number",
            new_name="customer_phone",
        ),
    ]
