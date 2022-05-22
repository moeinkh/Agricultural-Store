# Generated by Django 3.2.7 on 2022-05-22 07:35

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='عنوان بلاگ')),
                ('poster', models.ImageField(upload_to='product/blogs', verbose_name='پوستر بلاگ')),
                ('text', ckeditor.fields.RichTextField(verbose_name='متن بلاگ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')),
            ],
            options={
                'verbose_name': 'بلاگ',
                'verbose_name_plural': 'بلاگ ها',
            },
        ),
    ]
