# Generated by Django 4.2.4 on 2023-08-24 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainanalysis',
            name='http_status',
            field=models.PositiveIntegerField(null=True),
        ),
    ]