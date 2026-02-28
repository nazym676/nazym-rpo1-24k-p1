from .models import Category

def categories_processor(request):
    categories = Category.objects.all()
    return {
        'categories': categories,
        "bottom_categories": categories[:3],
        "menu_categories": categories
    }