# Generated by Django 5.1.2 on 2025-02-01 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0034_alter_order_adtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='customer.order'),
        ),
    ]
