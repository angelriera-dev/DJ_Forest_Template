import os
from typing import Any, cast

from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from apps.dashboard.models import SubscriptionPlan
from apps.users.models import User


class Command(BaseCommand):
    help = "Seed the database with initial data (admin user + subscription plans)"

    def handle(self, *args: Any, **options: Any) -> None:
        # Create admin user
        user, created = cast(
            tuple[User, bool],
            User.objects.get_or_create(
                email="admin@example.com",
                defaults={
                    "is_staff": True,
                    "is_superuser": True,
                    "first_name": "Admin",
                },
            ),
        )
        if created:
            password = os.environ.get(
                "DJANGO_SEED_ADMIN_PASSWORD"
            ) or get_random_string(16)
            validate_password(password, user=user)
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(  # type: ignore
                    f"Admin user created (admin@example.com / {password})"
                )
            )
        else:
            self.stdout.write("Admin user already exists")

        # Create subscription plans
        plans = [
            {
                "name": "Free",
                "slug": "free",
                "description": "Get started with the basics",
                "price": 0,
                "interval": "monthly",
                "features": ["Basic access", "Community support", "1 project"],
            },
            {
                "name": "Pro",
                "slug": "pro",
                "description": "For growing teams and businesses",
                "price": 9.99,
                "interval": "monthly",
                "features": [
                    "Everything in Free",
                    "Priority support",
                    "API access",
                    "10 projects",
                    "Analytics",
                ],
            },
            {
                "name": "Enterprise",
                "slug": "enterprise",
                "description": "For large-scale operations",
                "price": 49.99,
                "interval": "monthly",
                "features": [
                    "Everything in Pro",
                    "Dedicated support",
                    "Custom integrations",
                    "Unlimited projects",
                    "SLA guarantee",
                ],
            },
        ]

        for plan_data in plans:
            plan, created = SubscriptionPlan.objects.get_or_create(
                slug=plan_data["slug"],
                defaults=plan_data,
            )
            status = "created" if created else "already exists"
            self.stdout.write(self.style.SUCCESS(f'Plan "{plan.name}" {status}'))  # type: ignore

        self.stdout.write(self.style.SUCCESS("\nSeed data complete!"))  # type: ignore
