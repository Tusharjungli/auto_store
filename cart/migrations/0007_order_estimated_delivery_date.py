# Generated by Django 5.1.7 on 2025-03-16 17:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_order_created_at_alter_order_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='estimated_delivery_date',
            field=models.DateField(default=datetime.datetime(2025, 3, 21, 17, 7, 42, 30247, tzinfo=datetime.timezone.utc)),
        ),
    ]
