# Generated by Django 3.0.4 on 2021-01-15 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20210109_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookproduct',
            name='author_name',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='bookproduct',
            name='book_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookproduct',
            name='publication_year',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookproduct',
            name='publisher',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]