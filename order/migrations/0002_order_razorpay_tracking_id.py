# Generated by Django 5.1.1 on 2024-12-24 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='razorpay_tracking_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
