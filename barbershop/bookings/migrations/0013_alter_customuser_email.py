# Generated by Django 5.1.1 on 2024-09-28 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0012_remove_customuser_customer_phone_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="email address"
            ),
        ),
    ]
