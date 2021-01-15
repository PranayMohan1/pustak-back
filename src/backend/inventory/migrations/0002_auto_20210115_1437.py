# Generated by Django 3.0.4 on 2021-01-15 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend_settings', '0002_auto_20210115_1437'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookproduct',
            name='book_category',
        ),
        migrations.AddField(
            model_name='bookproduct',
            name='author_name',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='bookproduct',
            name='book_categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='book_category', to='backend_settings.Settings'),
        ),
        migrations.AddField(
            model_name='bookproduct',
            name='book_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookproduct',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bookproduct',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bookproduct',
            name='lang',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='language', to='backend_settings.Settings'),
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
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('is_approved', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('remarks', models.CharField(blank=True, max_length=1024, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approved_by', to=settings.AUTH_USER_MODEL)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.BookProduct')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]