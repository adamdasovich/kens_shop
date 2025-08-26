from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product
from videos.models import VideoCategory, Video
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Load sample data for development'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Create sample categories
        chair_category, _ = Category.objects.get_or_create(
            name="Chairs",
            defaults={'description': "Handcrafted chairs with exceptional comfort and style"}
        )
        
        stool_category, _ = Category.objects.get_or_create(
            name="Bar Stools",
            defaults={'description': "Elegant bar stools for any kitchen or bar area"}
        )
        
        # Create sample products
        products_data = [
            {
                'name': 'Classic Oak Dining Chair',
                'description': 'A timeless dining chair crafted from premium oak wood with a comfortable cushioned seat. Perfect for family dinners and special occasions.',
                'category': chair_category,
                'price': Decimal('485.00'),
                'status': 'available',
                'dimensions': '18" W x 20" D x 32" H',
                'materials': 'Oak wood, leather upholstery, brass hardware',
                'weight': Decimal('12.5'),
                'featured': True
            },
            {
                'name': 'Rustic Pine Bar Stool',
                'description': 'Handcrafted bar stool with a rustic charm, featuring distressed pine wood and iron accents.',
                'category': stool_category,
                'price': Decimal('225.00'),
                'status': 'available',
                'dimensions': '14" W x 14" D x 30" H',
                'materials': 'Pine wood, wrought iron, natural finish',
                'weight': Decimal('8.2'),
                'featured': True
            },
            {
                'name': 'Walnut Accent Chair',
                'description': 'Elegant accent chair made from rich walnut wood with intricate grain patterns and velvet upholstery.',
                'category': chair_category,
                'price': Decimal('650.00'),
                'status': 'sold',
                'dimensions': '26" W x 28" D x 34" H',
                'materials': 'Black walnut wood, velvet upholstery, brass studs',
                'weight': Decimal('18.3'),
                'featured': False
            },
            {
                'name': 'Industrial Bar Stool Set',
                'description': 'Set of two industrial-style bar stools combining reclaimed wood with steel framework.',
                'category': stool_category,
                'price': Decimal('380.00'),
                'status': 'in_progress',
                'dimensions': '15" W x 15" D x 28" H (each)',
                'materials': 'Reclaimed oak, powder-coated steel, matte finish',
                'weight': Decimal('22.0'),
                'featured': False
            },
            {
                'name': 'Cherry Wood Rocking Chair',
                'description': 'Traditional rocking chair crafted from solid cherry wood, perfect for porches and nurseries.',
                'category': chair_category,
                'price': Decimal('750.00'),
                'status': 'showcase',
                'dimensions': '28" W x 32" D x 42" H',
                'materials': 'Cherry wood, hand-rubbed oil finish',
                'weight': Decimal('25.8'),
                'featured': True
            }
        ]
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        # Create video categories
        process_category, _ = VideoCategory.objects.get_or_create(
            name="Crafting Process",
            defaults={'description': "Step-by-step videos showing the furniture creation process"}
        )
        
        technique_category, _ = VideoCategory.objects.get_or_create(
            name="Woodworking Techniques",
            defaults={'description': "Educational videos about woodworking methods and techniques"}
        )
        
        # Create sample video entries (you'll need to add actual video files)
        videos_data = [
            {
                'title': 'Crafting an Oak Dining Chair - Complete Process',
                'description': 'Watch the entire process of creating a classic oak dining chair from raw lumber to finished piece.',
                'category': process_category,
                'duration': 1800,  # 30 minutes
                'featured': True
            },
            {
                'title': 'Mortise and Tenon Joinery Techniques',
                'description': 'Learn the traditional mortise and tenon joint techniques used in fine furniture making.',
                'category': technique_category,
                'duration': 900,  # 15 minutes
                'featured': False
            },
            {
                'title': 'Wood Finishing: Oil vs. Polyurethane',
                'description': 'Comparison of different wood finishing techniques and when to use each one.',
                'category': technique_category,
                'duration': 720,  # 12 minutes
                'featured': True
            }
        ]
        
        for video_data in videos_data:
            video, created = Video.objects.get_or_create(
                title=video_data['title'],
                defaults=video_data
            )
            if created:
                self.stdout.write(f'Created video: {video.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )