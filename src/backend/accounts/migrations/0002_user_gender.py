# Generated by Django 3.0.4 on 2021-01-06 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
