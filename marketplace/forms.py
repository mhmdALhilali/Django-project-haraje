from django import forms
from .models import Advertisement, Message, Category, Governorate

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'price', 'category', 'governorate', 
                 'condition', 'contact_phone', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان الإعلان'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 
                                               'placeholder': 'وصف تفصيلي للمنتج'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'السعر بالريال اليمني'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'governorate': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موضوع الرسالة'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 
                                        'placeholder': 'نص الرسالة'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 
                                                        'placeholder': 'ابحث عن منتج...'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), 
                                     required=False, empty_label="جميع الفئات",
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    governorate = forms.ModelChoiceField(queryset=Governorate.objects.all(), 
                                        required=False, empty_label="جميع المحافظات",
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    price_min = forms.DecimalField(required=False, min_value=0,
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 
                                                                 'placeholder': 'أقل سعر'}))
    price_max = forms.DecimalField(required=False, min_value=0,
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 
                                                                 'placeholder': 'أعلى سعر'}))