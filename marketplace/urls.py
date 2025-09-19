from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
    path('category/<slug:category_slug>/', views.advertisement_list, 
         name='advertisement_list_by_category'),
    path('advertisement/<int:id>/<slug:slug>/', views.advertisement_detail, 
         name='advertisement_detail'),
    path('create/', views.advertisement_create, name='advertisement_create'),
    path('edit/<int:id>/', views.advertisement_edit, name='advertisement_edit'),
    path('my-ads/', views.my_advertisements, name='my_advertisements'),
    path('send-message/<int:advertisement_id>/', views.send_message, 
         name='send_message'),
    path('messages/', views.message_list, name='message_list'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
]