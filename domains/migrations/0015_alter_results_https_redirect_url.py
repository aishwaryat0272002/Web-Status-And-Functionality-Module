# Generated by Django 4.2.4 on 2023-10-06 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0014_rename_results_sagar_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='https_redirect_url',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]