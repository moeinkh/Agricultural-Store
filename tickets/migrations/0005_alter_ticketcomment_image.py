# Generated by Django 3.2.7 on 2021-10-13 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20211013_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketcomment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product/ticketcomment', verbose_name='عکس'),
        ),
    ]