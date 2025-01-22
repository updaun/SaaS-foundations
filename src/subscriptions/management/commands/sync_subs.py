from django.core.management.base import BaseCommand
from typing import Any

from subscriptions.models import Subscription


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        qs = Subscription.objects.filter(active=True)
        for obj in qs:
            sub_perms = obj.permissions.all()
            for group in obj.groups.all():
                group.permissions.set(sub_perms)
        self.stdout.write("Synced subscriptions")
