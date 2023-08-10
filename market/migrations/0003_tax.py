# Generated by Django 4.2.4 on 2023-08-10 02:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("market", "0002_rename_cart_cartitem"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tax",
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
                ("tax_type", models.CharField(max_length=16, unique=True)),
                (
                    "tax_percentage",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=4,
                        verbose_name="Tax Percentage (%)",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]
