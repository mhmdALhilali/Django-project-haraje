from django.contrib import admin
from .models import Category, Governorate, Advertisement, Message

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Governorate)
class GovernorateAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'governorate', 
                   'price', 'status', 'created']
    list_filter = ['status', 'category', 'governorate', 'condition', 'created']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    ordering = ['-created']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'created', 'read']
    list_filter = ['read', 'created']
    search_fields = ['subject', 'body']
    date_hierarchy = 'created'