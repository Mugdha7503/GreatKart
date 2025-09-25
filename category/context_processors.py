from .models import Category

def menu_links(request):
    links = Category.objects.all() #fetching all the category links 
    return dict(links=links)
