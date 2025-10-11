from django.shortcuts import render, get_object_or_404,redirect
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from accounts.decorators import seller_required
from .models import Product
from .forms import ProductForm

def store(request, category_slug=None):
    current_site = get_current_site(request)
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator=Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available= True).order_by('id')
        paginator=Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
    context={
        'products':paged_products,
        'product_count': product_count,
        'domain': current_site.domain,
    }
    return render(request,'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

        
    except Exception as e:
        raise e
    context={
        'single_product': single_product,
        'in_cart': in_cart,
        
    }

    return render(request, 'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:  #if get request is having the keyword or not. If it's true then we will use that keyword and store it.
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(desc__icontains=keyword) | Q(product_name__icontains=keyword)) #it will look for the whole desc
            product_count = products.count()
    context = {
        'products' : products,
        'product_count' :product_count,
    }
    return render(request,'store/store.html',context)




@login_required
def choose_role(request):
    if request.user.is_superadmin:
        # Superadmin sees both buttons
        return render(request, 'store/choose_role.html')

    if request.user.is_seller():
        return redirect('seller_dashboard')

    return redirect('buyer_home')

@login_required
@seller_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'store/seller_dashboard.html', {'products': products})

@login_required
def buyer_home(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'store/buyer_home.html', {'products': products})


@login_required
@seller_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})


@login_required
@seller_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('seller_dashboard')
    return render(request, 'store/edit_product.html', {'form': form})


@login_required
@seller_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('seller_dashboard')
    return render(request, 'store/delete_product.html', {'product': product})