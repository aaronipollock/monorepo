# Generated by Django 4.2.11 on 2024-04-17 05:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0011_client_clientprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="clientprofile",
            name="hmis_id",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]