# Generated by Django 4.1.4 on 2023-02-17 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_total_data_order_vendors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tax_data',
            field=models.JSONField(blank=True, help_text="Data format: {'tax_type': {'tax_percentage': 'tax_amount'}}", null=True),
        ),
    ]
