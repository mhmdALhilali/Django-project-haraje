from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Advertisement, Category, Message, Governorate
from .forms import AdvertisementForm, MessageForm, SearchForm

def advertisement_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    advertisements = Advertisement.objects.filter(status='active')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        advertisements = advertisements.filter(category=category)
    
    # البحث
    search_form = SearchForm()
    query = None
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            category_filter = search_form.cleaned_data['category']
            governorate_filter = search_form.cleaned_data['governorate']
            price_min = search_form.cleaned_data['price_min']
            price_max = search_form.cleaned_data['price_max']
            
            if query:
                advertisements = advertisements.filter(
                    Q(title__icontains=query) | Q(description__icontains=query)
                )
            if category_filter:
                advertisements = advertisements.filter(category=category_filter)
            if governorate_filter:
                advertisements = advertisements.filter(governorate=governorate_filter)
            if price_min:
                advertisements = advertisements.filter(price__gte=price_min)
            if price_max:
                advertisements = advertisements.filter(price__lte=price_max)
    
    # تقسيم الصفحات
    paginator = Paginator(advertisements, 12)
    page = request.GET.get('page')
    try:
        advertisements = paginator.page(page)
    except PageNotAnInteger:
        advertisements = paginator.page(1)
    except EmptyPage:
        advertisements = paginator.page(paginator.num_pages)
    
    return render(request, 'marketplace/advertisement/list.html',{'category': category, 'categories': categories,
                           'advertisements': advertisements,'search_form':    search_form,  'query':  query})
                 

def advertisement_detail(request, id, slug):
    advertisement = get_object_or_404(Advertisement, id=id, slug=slug, status='active')
    
    # إعلانات مشابهة
    related_ads = Advertisement.objects.filter(
        category=advertisement.category,
        status='active'
    ).exclude(id=advertisement.id)[:4]
    
    return render(request, 'marketplace/advertisement/detail.html',{'advertisement': advertisement,'related_ads': related_ads})

@login_required
def advertisement_create(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.seller = request.user
            advertisement.save()
            messages.success(request, 'تم نشر إعلانك بنجاح!')
            return redirect(advertisement.get_absolute_url())
    else:
        form = AdvertisementForm()
    
    return render(request, 'marketplace/advertisement/create.html',{'form': form})

@login_required
def advertisement_edit(request, id):
    advertisement = get_object_or_404(Advertisement, id=id, seller=request.user)
    
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث إعلانك بنجاح!')
            return redirect(advertisement.get_absolute_url())
    else:
        form = AdvertisementForm(instance=advertisement)
    
    return render(request, 'marketplace/advertisement/edit.html',{'form': form, 'advertisement': advertisement})

@login_required
def my_advertisements(request):
    advertisements = Advertisement.objects.filter(seller=request.user)
    
    paginator = Paginator(advertisements, 10)
    page = request.GET.get('page')
    try:
        advertisements = paginator.page(page)
    except PageNotAnInteger:
        advertisements = paginator.page(1)
    except EmptyPage:
        advertisements = paginator.page(paginator.num_pages)
    
    return render(request, 'marketplace/advertisement/my_ads.html',{'advertisements': advertisements})

@login_required
def send_message(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, id=advertisement_id, status='active')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.advertisement = advertisement
            message.sender = request.user
            message.recipient = advertisement.seller
            message.save()
            messages.success(request, 'تم إرسال رسالتك بنجاح!')
            return redirect(advertisement.get_absolute_url())
    else:
        form = MessageForm()
    
    # استخدم ملف موجود بالفعل
    return render(request, 'marketplace/advertisement/ads.html',{'form': form, 'advertisement': advertisement})

@login_required
def message_list(request):
    received_messages = Message.objects.filter(recipient=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    
    # استخدم ملف موجود بالفعل
    return render(request, 'marketplace/advertisement/list.html',
          {'received_messages': received_messages,'sent_messages': sent_messages})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    if message.recipient == request.user:
        message.read = True
        message.save()
    elif message.sender != request.user:
        return redirect('marketplace:message_list')
    
    # استخدم ملف موجود بالفعل
    return render(request, 'marketplace/advertisement/detail.html', {'message': message})
