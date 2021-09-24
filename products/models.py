from django.db import models
from django.utils import timezone
from django.utils.html import format_html

# Create your models here.
class Category(models.Model):

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='زیر دسته')
    name = models.CharField('نام', max_length=128)
    slug = models.SlugField('اسلاگ', max_length=128)
    image = models.ImageField('عکس', upload_to='product/category', null=True, blank=True,)

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)

    def __str__(self):
        return self.name

class Brand(models.Model):

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    name = models.CharField('نام', max_length=128)
    slug = models.SlugField('اسلاگ', max_length=128)
    image = models.ImageField('عکس', upload_to='product/brand', null=True, blank=True)

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته بندی')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='برند')

    name = models.CharField('نام', max_length=128)
    slug = models.SlugField('اسلاگ', max_length=128)
    image = models.ImageField('عکس محصول', upload_to='product/product', null=True, blank=True)
    country = models.CharField('کشور', max_length=128)
    weight = models.CharField('وزن', max_length=10, null=True, blank=True)
    volume = models.CharField('حجم', max_length=10, null=True, blank=True)
    formulation = models.CharField('فرمولاسیون', max_length=128, null=True, blank=True)
    packing = models.CharField('بسته بندی', max_length=64, null=True, blank=True)
    Elements = models.CharField('عناصر', max_length=128, null=True, blank=True)
    description = models.TextField('توضیحات')
    count = models.PositiveIntegerField('تعداد')
    price = models.PositiveIntegerField('قیمت')
    available = models.BooleanField('موجود', default=False)

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)


    def __str__(self):
        return self.name

    def image_tag(self):
        return format_html('<img src="{}" height="50" width="75" style="border-radius: 5px" />'.format(self.image.url))

    image_tag.short_description = 'عکس'    