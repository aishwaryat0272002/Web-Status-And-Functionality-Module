# Generated by Django 4.2.4 on 2023-08-24 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0002_alter_domainanalysis_http_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainanalysis',
            name='https_status',
            field=models.PositiveIntegerField(null=True),
        ),
    ]