from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from accounts.models import User
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from decimal import Decimal
from extensions.utils import jalali_converter


# Create your models here.
class Category(MPTTModel):

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='زیر دسته')
    name = models.CharField('نام', max_length=128)
    slug = models.SlugField('اسلاگ', allow_unicode=True, max_length=128)
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
    slug = models.SlugField('اسلاگ', allow_unicode=True, max_length=128)
    image = models.ImageField('عکس', upload_to='product/brand', null=True, blank=True)

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_list_brand', args=[self.slug])


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
    slug = models.SlugField('اسلاگ', allow_unicode=True, max_length=128)
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

    discount = models.IntegerField('درصد تخفیف', null=True, blank=True)
    befor_discount = models.PositiveIntegerField('قمیت قبل از تخفیف', null=True, blank=True)
    discount_status = models.BooleanField('وضعیت تخفیف', default=False)

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.count == 0:
            self.available = False
        elif self.count > 0:
            self.available = True    
   
        super().save(*args, **kwargs)      

    def image_tag(self):
        return format_html('<img src="{}" height="50" width="75" style="border-radius: 5px" />'.format(self.image.url))

    image_tag.short_description = 'عکس'   

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[str(self.id), self.slug]) 

        
    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ثبت'  

    def jupdated_at(self):
        return jalali_converter(self.updated_at)
    jupdated_at.short_description = 'تاریخ به روز شدن'      

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

        
    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ثبت'  

    def jupdated_at(self):
        return jalali_converter(self.updated_at)
    jupdated_at.short_description = 'تاریخ به روز شدن'  

class ProductHit(models.Model):
    class Meta:
        verbose_name = 'بازدید کننده های محصول'
        verbose_name_plural = 'بازدید کننده های محصولات'

    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip_address = models.ForeignKey('IpAddress', on_delete=models.CASCADE, verbose_name='آدرس آی پی')
    created_at = models.DateTimeField('تاریخ بازدید', auto_now_add=True)    

class Contact(models.Model):
    class Meta:
        verbose_name = 'پیام مخاطب'
        verbose_name_plural = 'پیام های مخاطبان'
        ordering = ['-created_at']

    name = models.CharField('نام', max_length=128)
    email = models.EmailField('ایمیل')
    text = models.TextField('متن پیام')

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)

    def __str__(self):
        return self.name 

    
    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ثبت'  

    def jupdated_at(self):
        return jalali_converter(self.updated_at)
    jupdated_at.short_description = 'تاریخ به روز شدن'       

class Banner(models.Model):
    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنر ها'
        ordering = ['-created_at']
    
    banner = models.ImageField('بنر', upload_to='product/banners')
    alt = models.CharField('متن تصویر', max_length=64)

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)

        
    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ثبت'  

    def jupdated_at(self):
        return jalali_converter(self.updated_at)
    jupdated_at.short_description = 'تاریخ به روز شدن'  

    def __str__(self):
        return self.alt