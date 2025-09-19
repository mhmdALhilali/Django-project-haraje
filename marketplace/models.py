from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم الفئة')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name='وصف الفئة')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'فئة'
        verbose_name_plural = 'الفئات'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('marketplace:advertisement_list_by_category', args=[self.slug])

class Governorate(models.Model):
    name = models.CharField(max_length=50, verbose_name='المحافظة')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'محافظة'
        verbose_name_plural = 'المحافظات'
    
    def __str__(self):
        return self.name

class Advertisement(models.Model):
    STATUS_CHOICES = [
        ('active', 'نشط'),
        ('sold', 'مباع'),
        ('expired', 'منتهي الصلاحية'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'جديد'),
        ('used_excellent', 'مستعمل - ممتاز'),
        ('used_good', 'مستعمل - جيد'),
        ('used_fair', 'مستعمل - مقبول'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='عنوان الإعلان')
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(verbose_name='وصف الإعلان')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                related_name='advertisements', verbose_name='الفئة')
    governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE, 
                                   verbose_name='المحافظة')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name='advertisements', verbose_name='البائع')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, 
                                default='used_good', verbose_name='حالة المنتج')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                             default='active', verbose_name='حالة الإعلان')
    contact_phone = models.CharField(max_length=15, verbose_name='رقم الهاتف')
    image = models.ImageField(upload_to='advertisements/%Y/%m/%d/', 
                             blank=True, verbose_name='صورة المنتج')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ النشر')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'إعلان'
        verbose_name_plural = 'الإعلانات'
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('marketplace:advertisement_detail', args=[self.id, self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Message(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, 
                                     related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name='received_messages')
    subject = models.CharField(max_length=200, verbose_name='الموضوع')
    body = models.TextField(verbose_name='نص الرسالة')
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False, verbose_name='مقروءة')
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'رسالة'
        verbose_name_plural = 'الرسائل'
    
    def __str__(self):
        return f'رسالة من {self.sender} إلى {self.recipient}'