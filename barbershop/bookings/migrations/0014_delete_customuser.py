# Generated by Django 5.1.1 on 2024-09-28 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0013_alter_customuser_email"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CustomUser",
        ),
    ]