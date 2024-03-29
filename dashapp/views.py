from datetime import datetime
from django.db.models.aggregates import Count
from django.http import response, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .filters import StocktakingFilter
from .forms import CategoryForm, MeasuredForm, LocationForm, ProductForm
from django.utils import timezone
import csv
import datetime

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

    #Get the current date 
    current_date = timezone.now()
    dates = stocktaking_tb.objects.filter(expiration_date=current_date).count()
    
    total_cate = categories.count()
    total_mea = measureds.count()
    total_loc = locations.count()

    myFilter = StocktakingFilter()

    context_va = {'products':products, 'categories':categories, 'measureds':measureds, 'locations':locations, 'total_cate':total_cate, 'total_mea':total_mea, 'total_loc':total_loc,'expiration_products':dates ,'myFilter':myFilter}

    return render(request,'dash.html', context_va)

# url = http://localhost:8000/dashapp/dash/

def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Productos'+ \
        str(datetime.datetime.now())+'.csv'
    
    writer=csv.writer(response)
    writer.writerow(['SKU_id','CATE_id','MEA_id','LOC_id','description_product','brand_product','final_price_list','quantity_product','expiration_date','agregation_date','lastupdated_date','cost_unit'])

    products = stocktaking_tb.objects.filter(SKU_id=request.user)

    for product in products:
        writer.writerow([product.SKU_I, product.CATE_id, product.MEA_id, product.LOC_id, product.description_product, product.brand_product, product.final_price_list, product.quantity_product, product.expiration_date, product.agregation_date, product.lastupdated_date, product.cost_unit])

    return response

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

# Vista del form para añadir una ubicacion (requieres estar logueado para accder)
@login_required
def createLocationView(request):
    form = LocationForm()
    
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('dashboardView')

    context = {'form':form}
    return render(request,'location_form.html', context)

# Vista del form para actualizar ubicaciones (requieres estar logueado para accder)
@login_required
def updateLocationView(request, pk):
    location =location_catalog.objects.get(LOC_id=pk)
    form =LocationForm(instance=location)

    if request.method == 'POST':
        form = LocationForm(request.POST,instance=location)
        if form.is_valid():
            form.save()
            #return redirect('dashboardView')

    context = {'form':form}
    return render(request,'location_form.html', context)