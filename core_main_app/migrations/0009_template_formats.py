# Generated by Django 4.2.3 on 2023-07-27 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core_main_app", "0008_blob_ordering"),
    ]

    operations = [
        migrations.RenameField(
            model_name="data",
            old_name="xml_file",
            new_name="file",
        ),
        migrations.RenameField(
            model_name="template",
            old_name="hash",
            new_name="_hash",
        ),
        migrations.AddField(
            model_name="template",
            name="format",
            field=models.CharField(
                choices=[("XSD", "XML Schema"), ("JSON", "JSON Schema")],
                default="XSD",
                max_length=20,
            ),
        ),
    ]
