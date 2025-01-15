# Generated by Django 5.0.9 on 2025-01-14 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_medicalprofessional_is_medical_professional_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='type',
            field=models.CharField(choices=[('PATIENT', 'patient'), ('MEDICALPROFESSIONAL', 'medicalprofessional')], max_length=25, null=True),
        ),
    ]
