# Generated by Django 5.0.7 on 2024-08-12 21:19

import clients.enums
import django.db.models.deletion
import django_choices_field.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0028_clientcontact"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientHouseholdMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "gender",
                    django_choices_field.fields.TextChoicesField(
                        blank=True,
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("non_binary", "Non-binary"),
                            ("other", "Other"),
                            ("prefer_not_to_say", "Prefer not to say"),
                        ],
                        choices_enum=clients.enums.GenderEnum,
                        max_length=17,
                        null=True,
                    ),
                ),
                (
                    "relationship_to_client",
                    django_choices_field.fields.TextChoicesField(
                        blank=True,
                        choices=[
                            ("current_case_manager", "Current Case Manager"),
                            ("past_case_manager", "Past Case Manager"),
                            ("organization", "Organization"),
                            ("aunt", "Aunt"),
                            ("child", "Child"),
                            ("cousin", "Cousin"),
                            ("father", "Father"),
                            ("friend", "Friend"),
                            ("grandparent", "Grandparent"),
                            ("mother", "Mother"),
                            ("pet", "Pet"),
                            ("sibling", "Sibling"),
                            ("uncle", "Uncle"),
                            ("other", "Other"),
                        ],
                        choices_enum=clients.enums.RelationshipTypeEnum,
                        max_length=20,
                        null=True,
                    ),
                ),
                ("relationship_to_client_other", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "client_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="household_members",
                        to="accounts.clientprofile",
                    ),
                ),
            ],
        ),
    ]
