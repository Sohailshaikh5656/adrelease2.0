# Generated by Django 5.1.2 on 2025-03-01 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0053_alter_order_any_preferance'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencyprofile',
            name='cm_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
