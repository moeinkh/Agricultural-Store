# Generated by Django 3.2.7 on 2021-10-09 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='befor_discount',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='قمیت قبل از تخفیف'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.IntegerField(blank=True, null=True, verbose_name='درصد تخفیف'),
        ),
    ]
