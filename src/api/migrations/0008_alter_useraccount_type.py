# Generated by Django 5.0.9 on 2025-01-14 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_useraccount_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='type',
            field=models.CharField(choices=[('PATIENT', 'patient'), ('MEDICALPROFESSIONAL', 'medicalprofessional'), ('ADMIN', 'admin')], max_length=25, null=True),
        ),
    ]
