# Generated by Django 3.2.7 on 2021-10-09 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20211010_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_status',
            field=models.BooleanField(blank=True, null=True, verbose_name='وضعیت تخفیف'),
        ),
    ]
