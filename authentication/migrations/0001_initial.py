# Generated by Django 4.2 on 2024-02-02 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('uid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'default_related_name': 'users',
            },
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('uid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('type', models.CharField(blank=True, choices=[('personal', 'Personal'), ('business', 'Business'), ('owner', 'Owner')], default=None, max_length=8, null=True, verbose_name='Type')),
                ('registration_date', models.DateTimeField(auto_now_add=True, verbose_name='Registration Date')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Last Login')),
                ('security_key', models.BinaryField(blank=True, null=True, verbose_name='Security Key')),
            ],
            options={
                'default_related_name': 'tenants',
            },
        ),
        migrations.CreateModel(
            name='TenantUserRequest',
            fields=[
                ('uid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default=None, max_length=8, null=True, verbose_name='Status')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TenantUserInvitation',
            fields=[
                ('uid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default=None, max_length=8, null=True, verbose_name='Status')),
                ('role', models.CharField(blank=True, choices=[('Owner', 'Owner'), ('Admin', 'Admin'), ('User', 'User')], default=None, max_length=5, null=True, verbose_name='Role')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accepted_at', models.DateTimeField(blank=True, null=True)),
                ('rejected_at', models.DateTimeField(blank=True, null=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.tenant')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TenantUser',
            fields=[
                ('uid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, choices=[('Owner', 'Owner'), ('Admin', 'Admin'), ('User', 'User')], default=None, max_length=5, null=True, verbose_name='Role')),
                ('is_active', models.BooleanField(default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]