# Generated by Django 5.1.7 on 2025-03-28 17:10

from clients.permissions import SocialMediaProfilePermissions
from django.db import migrations


def create_permissions_if_not_exist(apps, schema_editor):
    SocialMediaProfile = apps.get_model("clients", "SocialMediaProfile")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    SocialMediaProfileContentType = ContentType.objects.get_for_model(SocialMediaProfile)
    db_alias = schema_editor.connection.alias

    # Generate readable names based on the enum
    PERM_MAP = {perm.split(".")[1]: perm.label for perm in SocialMediaProfilePermissions}
    for codename, name in PERM_MAP.items():
        Permission.objects.using(db_alias).get_or_create(
            codename=codename,
            content_type=SocialMediaProfileContentType,
            defaults={"name": name, "content_type": SocialMediaProfileContentType},
        )


def update_caseworker_permission_template(apps, schema_editor):
    PermissionGroupTemplate = apps.get_model("accounts", "PermissionGroupTemplate")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    SocialMediaProfile = apps.get_model("clients", "SocialMediaProfile")
    SocialMediaProfileContentType = ContentType.objects.get_for_model(SocialMediaProfile)
    caseworker_template = PermissionGroupTemplate.objects.get(name="Caseworker")

    perm_map = [
        perm.split(".")[1]
        for perm in [
            "clients.add_socialmediaprofile",
            "clients.view_socialmediaprofile",
            "clients.change_socialmediaprofile",
            "clients.delete_socialmediaprofile",
        ]
    ]

    permissions = Permission.objects.filter(codename__in=perm_map, content_type=SocialMediaProfileContentType)
    caseworker_template.permissions.add(*permissions)


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0026_clienthouseholdmember_permissions"),
    ]

    operations = [
        migrations.RunPython(create_permissions_if_not_exist),
        migrations.RunPython(update_caseworker_permission_template),
    ]
