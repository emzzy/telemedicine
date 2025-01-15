# Generated by Django 5.0.9 on 2025-01-13 00:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_medicalprofessional_options_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalprofessional',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='medicalprofessional',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='medicalprofessional',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='medicalprofessional',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='medicalprofessional',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='date_joined',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='date_of_birth',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='gender',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='location',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='type',
            field=models.CharField(choices=[('PATIENT', 'patient'), ('MEDICALPROFESSIONAL', 'medicalprofessional')], default='PATIENT', max_length=25),
        ),
        migrations.AlterField(
            model_name='medicalprofessional',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='first_name',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='last_name',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
