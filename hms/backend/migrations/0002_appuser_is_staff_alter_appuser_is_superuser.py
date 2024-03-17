# Generated by Django 5.0.3 on 2024-03-17 09:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appuser",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="appuser",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
    ]