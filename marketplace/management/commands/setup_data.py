from django.core.management.base import BaseCommand
from marketplace.models import Category, Governorate

class Command(BaseCommand):
    help = 'إعداد البيانات الأولية للموقع'

    def handle(self, *args, **options):
        # إضافة الفئات
        categories = [
            {'name': 'عقارات', 'slug': 'real-estate', 'description': 'شقق، فلل، أراضي، محلات'},
            {'name': 'مركبات', 'slug': 'vehicles', 'description': 'سيارات، دراجات نارية، شاحنات'},
            {'name': 'إلكترونيات', 'slug': 'electronics', 'description': 'جوالات، كمبيوترات، تلفزيونات'},
            {'name': 'أثاث ومنزل', 'slug': 'furniture', 'description': 'أثاث، أجهزة منزلية، ديكور'},
            {'name': 'سوق يمني تقليدي', 'slug': 'traditional', 'description': 'عسل، بن، حرف يدوية'},
            {'name': 'وظائف وخدمات', 'slug': 'jobs-services', 'description': 'وظائف، خدمات، أعمال حرة'},
            {'name': 'حيوانات', 'slug': 'animals', 'description': 'مواشي، طيور، حيوانات أليفة'},
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'تم إنشاء فئة: {category.name}')

        # إضافة المحافظات
        governorates = [
            'صنعاء', 'عدن', 'تعز', 'الحديدة', 'إب', 'ذمار', 'حضرموت',
            'المحويت', 'حجة', 'صعدة', 'عمران', 'البيضاء', 'لحج',
            'أبين', 'شبوة', 'المهرة', 'الجوف', 'مأرب', 'الضالع',
            'ريمة', 'سقطرى'
        ]

        for gov_name in governorates:
            governorate, created = Governorate.objects.get_or_create(name=gov_name)
            if created:
                self.stdout.write(f'تم إنشاء محافظة: {governorate.name}')

        self.stdout.write(self.style.SUCCESS('تم إعداد البيانات الأولية بنجاح!'))