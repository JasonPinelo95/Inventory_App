from django.db.models.aggregates import Count
from django.shortcuts import render, redirect
from .models import *
from .filters import StocktakingFilter
from .forms import ProductForm
#from .urls import *
from django.contrib.auth.decorators import login_required
# from .forms import 

# Create your views here.
# Vista del dashboard de dashapp (reuiqeres estar logueado para acceder)
@login_required
def dashboardView(request):
    products = stocktaking_tb.objects.all()
    categories = category_catalog.objects.all()
    measureds = measured_catalog.objects.all()
    locations = location_catalog.objects.all()
    
    total_cate = categories.count()
    total_mea = measureds.count()
    total_loc = locations.count()

    myFilter = StocktakingFilter()

    context_va = {'products':products, 'total_cate':total_cate, 'total_mea':total_mea, 'total_loc':total_loc, 'myFilter':myFilter}

    return render(request,'dash.html', context_va)

# url = http://localhost:8000/dashapp/dash/

# Vista de los productos de appdash in (reuiqeres estar logueado para acceder)
@login_required
def productView(request):
    return render(request,'products.html')
# url = http://localhost:8000/dashapp/products/

# Vista del form para añadir productos (requieres estar logueado para accder)
@login_required
def createProductView(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('dashboardView')

    context = {'form':form}
    return render(request,'product_form.html', context)
# url = http://localhost:8000/dashapp/formProducts/

# Vista del form para actualizar productos (requieres estar logueado para accder)
@login_required
def updateProductView(request, pk):
    product =stocktaking_tb.objects.get(SKU_id=pk)
    form =ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            #return redirect('dashboardView')

    context = {'form':form}
    return render(request,'product_form.html', context)

 # Vista del form para eliminar un productos (requieres estar logueado para accder)
@login_required
def removeProductView(request, pk):
    product =stocktaking_tb.objects.get(SKU_id=pk)
    if request.method == 'POST':
        product.delete()
        #return redirect('dashboardView')
    context = {'item':product}
    return render(request,'delete_product.html', context)