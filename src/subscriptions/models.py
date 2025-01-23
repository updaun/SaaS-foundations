import helpers.billing
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings


User = settings.AUTH_USER_MODEL  # "auth.User"

ALLOW_CUSTOM_GROUPS = True
SUBSCRIPTION_PERMISSIONS = [
    ("advanced", "Advanced Perm"),  # subscription.advanced
    ("pro", "Pro Perm"),  # subscription.pro
    ("basic", "Basic Perm"),  # subscription.basic
    ("basic_ai", "Basic AI Perm"),  # subscription.basic_ai
]


class Subscription(models.Model):
    """
    Subscription Plan = Stripe Product
    """

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
    stripe_id = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.stripe_id:
            stripe_id = helpers.billing.create_product(
                raw=False,
                name=self.name,
                metadata={
                    "subscription_plan_id": self.id,
                },
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)


class SubscriptionPrice(models.Model):
    """
    Subscription Price = Stripe Price
    """

    class IntervalChoices(models.TextChoices):
        MONTHLY = "month", "Monthly"
        YEARLY = "year", "Yearly"

    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, null=True, blank=True
    )
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    interval = models.CharField(
        max_length=120, default=IntervalChoices.MONTHLY, choices=IntervalChoices.choices
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)

    @property
    def stripe_currency(self):
        return "usd"

    @property
    def stripe_price(self):
        """
        remove decimal places
        """
        return self.price * 100

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id

    def save(self, *args, **kwargs):
        if self.stripe_id is None and self.product_stripe_id is not None:
            stripe_id = helpers.billing.create_price(
                currency=self.stripe_currency,
                product_id=self.product_stripe_id,
                unit_amount=self.stripe_price,
                interval=self.interval,
                metadata={
                    "subscription_plan_price_id": self.id,
                },
                raw=False,
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, null=True, blank=True
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.subscription}"


def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups_ids = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list("id", flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups_ids)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups = subs_qs.values_list("groups__id", flat=True)
        subs_groups_set = set(subs_groups)
        current_groups = user.groups.all().values_list("id", flat=True)
        groups_ids_set = set(groups_ids)
        current_groups_set = set(current_groups) - subs_groups_set
        final_group_ids = list(groups_ids_set | current_groups_set)
        user.groups.set(final_group_ids)


post_save.connect(user_sub_post_save, sender=UserSubscription)
