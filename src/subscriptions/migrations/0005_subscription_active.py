# Generated by Django 5.0.9 on 2024-12-26 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_alter_subscription_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]