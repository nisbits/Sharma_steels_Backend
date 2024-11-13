# Generated by Django 5.1.1 on 2024-11-13 04:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_alter_cartitem_price_alter_cartitem_quantity"),
        ("products", "0007_extracharge_amount_known"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderSummary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "total_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderSummaryItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "total_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "extra_charges",
                    models.ManyToManyField(
                        blank=True,
                        related_name="order_items",
                        to="products.extracharge",
                    ),
                ),
                (
                    "order_summary",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="cart.ordersummary",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]