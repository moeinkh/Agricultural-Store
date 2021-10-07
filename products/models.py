from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from accounts.models import User
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

# Create your models here.
class Category(MPTTModel):

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='زیر دسته')
    name = models.CharField('نام', max_length=128)
    slug = models.SlugField('اسلاگ', max_length=128)
    image = models.ImageField('عکس', upload_to='product/category', null=True, blank=True,)

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)

    def __str__(self):
        return self.name    

    def get_absolute_url(self):
        return reverse('product:product_list_category', args=[self.slug])

    class MPTTMeta:
        order_insertion_by = ['name']    

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


class IpAddress(models.Model):

    class Meta:
        verbose_name = 'بازدید'
        verbose_name_plural = 'بازدید ها'

    ip_address = models.GenericIPAddressField('آدرس آی پی')

    def __str__(self):
        return self.ip_address



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
    low_description = models.TextField('توضیحات مختصر')
    count = models.PositiveIntegerField('تعداد')
    price = models.PositiveIntegerField('قیمت')
    available = models.BooleanField('موجود', default=False)
    total_description = RichTextField('توضیحات کامل')

    hits = models.ManyToManyField(IpAddress, blank=True, related_name='hits', verbose_name='بازدید ها')

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.count == 0:
            self.available = False
        super().save(*args, **kwargs)      

    def image_tag(self):
        return format_html('<img src="{}" height="50" width="75" style="border-radius: 5px" />'.format(self.image.url))

    image_tag.short_description = 'عکس'   

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[str(self.id), self.slug]) 

class Images(models.Model):
    class Meta:
        verbose_name = 'عکس'
        verbose_name_plural = 'عکس ها'  

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    title = models.CharField('عنوان', max_length=128)
    image = models.ImageField('عکس', upload_to='product/product/gallery')

    def __str__(self):
        return self.title

class Comment(models.Model):
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    comment = models.TextField('نظر')
    active = models.BooleanField('فعال', default=True)

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)

    def __str__(self):
        return f'{self.user.username} برای {self.product.name}'

class ProductHit(models.Model):
    class Meta:
        verbose_name = 'بازدید کننده های محصول'
        verbose_name_plural = 'بازدید کننده های محصولات'

    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip_address = models.ForeignKey('IpAddress', on_delete=models.CASCADE, verbose_name='آدرس آی پی')
    created_at = models.DateTimeField('تاریخ بازدید', auto_now_add=True)    