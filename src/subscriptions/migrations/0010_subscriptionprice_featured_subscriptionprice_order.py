# Generated by Django 5.0.10 on 2025-01-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0009_subscriptionprice"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptionprice",
            name="featured",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="subscriptionprice",
            name="order",
            field=models.IntegerField(default=-1),
        ),
    ]
