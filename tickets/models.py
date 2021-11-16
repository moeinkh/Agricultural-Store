from django.db import models
from accounts.models import User
from extensions.utils import jalali_converter
from django.urls import reverse

# Create your models here.
class Ticket(models.Model):
    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'
        ordering = ['-updated_at']

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')

    GARDENING = 1
    AGRICULTURE = 2
    SALES = 3
    SUBJECT_CHOICES = (
        (GARDENING, 'باغبانی'),
        (AGRICULTURE, 'کشاورزی'),
        (SALES, 'فروش'),
    )
    subject = models.IntegerField('موضوع', choices=SUBJECT_CHOICES)
    text = models.TextField('متن')
    image = models.ImageField('عکس', upload_to='product/ticket', null=True, blank=True)

    OPEN = 1
    PENDING = 2
    ANSWERD = 3
    CLOSED  = 4

    STATUS_CHOICES = (
        (OPEN, 'باز'),
        (PENDING, 'در حال بررسی'),
        (ANSWERD, 'پاسخ داده شده'),
        (CLOSED, 'بسته شده'),
    )
    status = models.IntegerField('وضعیت', choices=STATUS_CHOICES, default=1)

    
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)
    
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('ticket:ticket_details', args=[str(self.id)])    

    
    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ثبت'  

    def jupdated_at(self):
        return jalali_converter(self.updated_at)
    jupdated_at.short_description = 'تاریخ به روز کردن '     

class TicketComment(models.Model):
    class Meta:
        verbose_name = 'جواب تیکت'
        verbose_name_plural = 'جواب های تیکت'
        ordering = ['-updated_at']  

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments', verbose_name='تیکت')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    text = models.TextField('متن')
    image = models.ImageField('عکس', upload_to='product/ticketcomment', null=True, blank=True)      

    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروز رسانی', auto_now=True)

    def __str__(self):
        return self.ticket.user.username

    
    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ سفارش'  

    def jupdated_at(self):
        return jalali_converter(self.updated_at)
    jupdated_at.short_description = 'تاریخ به روز کردن سفارش'     