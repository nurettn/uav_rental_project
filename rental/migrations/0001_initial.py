# Generated by Django 5.1.5 on 2025-01-22 11:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Aircraft",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        choices=[("TB2", "TB2"), ("TB3", "TB3"), ("AKINCI", "AKINCI"), ("KIZILELMA", "KIZILELMA")],
                        max_length=50,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("Wing", "Wing Team"),
                            ("Fuselage", "Fuselage Team"),
                            ("Tail", "Tail Team"),
                            ("Avionics", "Avionics Team"),
                            ("Assembly", "Assembly Team"),
                        ],
                        max_length=50,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Part",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "part_type",
                    models.CharField(
                        choices=[
                            ("Wing", "Wing"),
                            ("Fuselage", "Fuselage"),
                            ("Tail", "Tail"),
                            ("Avionics", "Avionics"),
                        ],
                        max_length=50,
                    ),
                ),
                ("stock", models.PositiveIntegerField(default=0)),
                (
                    "aircraft",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="parts", to="rental.aircraft"
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="parts", to="rental.team"
                    ),
                ),
            ],
            options={
                "unique_together": {("part_type", "aircraft", "team")},
            },
        ),
        migrations.CreateModel(
            name="Assembly",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("assembled_at", models.DateTimeField(auto_now_add=True)),
                (
                    "aircraft",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="assemblies", to="rental.aircraft"
                    ),
                ),
                (
                    "avionics",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="assembled_avionics", to="rental.part"
                    ),
                ),
                (
                    "fuselages",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="assembled_fuselages",
                        to="rental.part",
                    ),
                ),
                (
                    "tails",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="assembled_tails", to="rental.part"
                    ),
                ),
                (
                    "wings",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="assembled_wings", to="rental.part"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Personnel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
                (
                    "team",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="personnel",
                        to="rental.team",
                    ),
                ),
            ],
        ),
    ]
