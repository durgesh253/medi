# Generated by Django 5.0.1 on 2024-01-18 07:13

import app.utils.file_helpers
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile', models.ImageField(default='default-images\\default-profile.png', upload_to=app.utils.file_helpers.custom_file_name)),
                ('staff_id', models.CharField(editable=False, max_length=10, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('mobile', models.CharField(max_length=50, null=True)),
                ('password', models.CharField(blank=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('otp', models.CharField(default='123456', max_length=20)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.role')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
    ]