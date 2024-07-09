# Generated by Django 5.0.6 on 2024-07-08 15:29

import django.db.models.deletion
import django_choices_field.fields
import shelters.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shelters", "0003_shelter_hero_image_alter_shelter_phone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="requirement",
            name="shelter",
        ),
        migrations.RemoveField(
            model_name="shelter",
            name="image_url",
        ),
        migrations.RemoveField(
            model_name="shelter",
            name="typical_stay_description",
        ),
        migrations.AddField(
            model_name="shelter",
            name="intake_process",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name="funder",
            unique_together={("title", "shelter")},
        ),
        migrations.AlterUniqueTogether(
            name="population",
            unique_together={("title", "shelter")},
        ),
        migrations.AlterUniqueTogether(
            name="service",
            unique_together={("title", "shelter")},
        ),
        migrations.AlterUniqueTogether(
            name="sheltertype",
            unique_together={("title", "shelter")},
        ),
        migrations.CreateModel(
            name="EntryRequirement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "title",
                    django_choices_field.fields.TextChoicesField(
                        choices=[
                            ("Photo ID", "Photo ID"),
                            ("Medicaid or Medicare", "Medicaid or Medicare"),
                            ("Reservation", "Reservation"),
                            ("Referral", "Referral"),
                        ],
                        choices_enum=shelters.enums.EntryRequirements,
                        max_length=20,
                    ),
                ),
                (
                    "shelter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="requirements", to="shelters.shelter"
                    ),
                ),
            ],
            options={
                "unique_together": {("title", "shelter")},
            },
        ),
        migrations.CreateModel(
            name="PetsAllowed",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "title",
                    django_choices_field.fields.TextChoicesField(
                        choices=[
                            ("Service Animal", "Service Animal"),
                            ("Cats", "Cats"),
                            ("Emotional Support", "Emotional Support"),
                            ("Dogs <25lbs", "Dogs <25lbs"),
                            ("Dogs >25lbs", "Dogs >25lbs"),
                            ("Exotics", "Exotics"),
                        ],
                        choices_enum=shelters.enums.PetsAllowedEnum,
                        max_length=17,
                    ),
                ),
                (
                    "shelter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="pets_allowed", to="shelters.shelter"
                    ),
                ),
            ],
            options={
                "unique_together": {("title", "shelter")},
            },
        ),
        migrations.DeleteModel(
            name="HowToEnter",
        ),
        migrations.DeleteModel(
            name="Requirement",
        ),
    ]