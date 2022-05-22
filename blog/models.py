from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Blog(models.Model):
    class Meta:
        verbose_name = 'بلاگ'
        verbose_name_plural = 'بلاگ ها'

    title = models.CharField('عنوان بلاگ', max_length=128)
    slug = models.SlugField('اسلاگ بلاگ', allow_unicode=True, max_length=128)
    poster = models.ImageField('پوستر بلاگ', upload_to='product/blogs')
    text = RichTextField('متن بلاگ')


    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)

    def __str__(self):
        return self.title