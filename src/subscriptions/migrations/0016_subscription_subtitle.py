# Generated by Django 5.0.10 on 2025-01-24 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0015_subscription_features"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="subtitle",
            field=models.TextField(blank=True, null=True),
        ),
    ]
