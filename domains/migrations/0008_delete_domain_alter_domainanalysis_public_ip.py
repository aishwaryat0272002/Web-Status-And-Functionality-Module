# Generated by Django 4.2.4 on 2023-09-01 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0007_domain'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Domain',
        ),
        migrations.AlterField(
            model_name='domainanalysis',
            name='public_ip',
            field=models.CharField(default='N/A', max_length=15),
        ),
    ]
