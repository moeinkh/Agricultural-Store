# Generated by Django 3.2.7 on 2021-10-07 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128, unique=True, verbose_name='کد')),
                ('discount', models.IntegerField(verbose_name='تخفیف')),
                ('valid_from', models.DateTimeField(verbose_name='از تاریخ')),
                ('valid_to', models.DateTimeField(verbose_name='تا تاریخ')),
                ('active', models.BooleanField(verbose_name='فعال؟')),
            ],
            options={
                'verbose_name': 'کد تخفیف',
                'verbose_name_plural': 'کد های تخفیف',
            },
        ),
    ]
