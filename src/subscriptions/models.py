from django.db import models
from django.contrib.auth.models import Group, Permission


SUBSCRIPTION_PERMISSIONS = [
    ("advanced", "Advanced Perm"),  # subscription.advanced
    ("pro", "Pro Perm"),  # subscription.pro
    ("basic", "Basic Perm"),  # subscription.basic
    ("basic_ai", "Basic AI Perm"),  # subscription.basic_ai
]


class Subscription(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(
        Permission,
        limit_choices_to={
            "content_type__app_label": "subscriptions",
            "codename__in": [perm[0] for perm in SUBSCRIPTION_PERMISSIONS],
        },
    )

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS

    def __str__(self):
        return self.name
