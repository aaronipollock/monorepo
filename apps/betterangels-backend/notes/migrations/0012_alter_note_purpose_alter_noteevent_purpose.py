# Generated by Django 5.1.2 on 2024-10-14 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0011_remove_servicerequest_service_request_add_insert_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="note",
            name="purpose",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="noteevent",
            name="purpose",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]