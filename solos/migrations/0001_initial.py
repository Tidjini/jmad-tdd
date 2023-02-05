# Generated by Django 4.1.5 on 2023-02-01 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Solo",
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
                ("track", models.CharField(max_length=50)),
                ("artist", models.CharField(max_length=50)),
                ("instrument", models.CharField(max_length=100)),
            ],
        ),
    ]