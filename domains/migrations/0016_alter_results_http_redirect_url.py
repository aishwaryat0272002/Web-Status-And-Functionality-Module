# Generated by Django 4.2.4 on 2023-10-06 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0015_alter_results_https_redirect_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='http_redirect_url',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]