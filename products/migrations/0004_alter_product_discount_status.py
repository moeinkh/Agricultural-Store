# Generated by Django 3.2.7 on 2021-10-12 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_discount_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_status',
            field=models.BooleanField(default=False, verbose_name='وضعیت تخفیف'),
        ),
    ]