# Generated by Django 5.0.6 on 2024-05-14 23:54

import django.contrib.gis.db.models.fields
from django.db import migrations
from django.contrib.gis.geos import Point


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0012_alter_locationuserobjectpermission_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="point",
            field=django.contrib.gis.db.models.fields.PointField(
                default=Point(-118.2437207, 34.0521723), geography=True, srid=4326
            ),
            preserve_default=False,
        ),
    ]