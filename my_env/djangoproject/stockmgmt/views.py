from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
import csv
from django.urls import reverse
from stockmgmt.models import Stock, StockHistory,Category
from stockmgmt.forms import StockCreateForm, StockSearchForm,StockHistorySearchForm, StockUpdateForm, ExportForm, ImportForm, ReorderLevelForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    title = 'Welcome: This is the Home Page'
    dict = {
        'title':title
    }
    return HttpResponseRedirect(reverse('list_items'))
    # return render(request, 'home.html', context=dict)

def login_page(request):
    title = 'Login To Stock Application'
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

    return render(request, 'login.html', context={'title':title, 'form':form})

@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_page'))

@login_required
def list_items(request):
    title = 'List of Stock Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    dict = {'title': title ,'form':form, 'queryset':queryset}

    if request.method == 'POST':
        category = form['category'].value()
        queryset = StockHistory.objects.filter(item_name__icontains=form['item_name'].value())
        if (category != ''):
            queryset = queryset.filter(category_id=category)

        dict = {'title': title,'form':form, 'queryset':queryset}

        if form['export_to_CSV'].value()==True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition']='attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY','ITEM NAME','QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
    return render(request, 'list_items.html', context=dict)

@login_required
def list_history(request):
    title = 'EXPORT / IMPORT  HISTORY'
    queryset = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST or None)
    dict = {'title':title, 'queryset':queryset , 'form':form}
    if request.method == 'POST':
        category = form['category'].value()
        queryset = StockHistory.objects.filter(
                                	item_name__icontains=form['item_name'].value(),
                                	last_updated__range=[
                                							form['start_date'].value(),
                                							form['end_date'].value()
                                						]
                                	)
        if (category != ''):
            queryset = queryset.filter(category_id=category)

        if form['export_to_CSV'].value()==True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition']='attachment; filename="Export Import History.csv"'
            writer = csv.writer(response)
            writer.writerow([
                'CATEGORY',
                'ITEM NAME',
                'QUANTITY',
                'EXPORT QUANTITY',
                'IMPORT QUANTITY',
                'EXPORT BY',
                'IMPORT BY',
                'LAST UPDATED'
                ])
            instance = queryset
            for stock in instance:
                writer.writerow([
                    stock.category,
                    stock.item_name,
                    stock.quantity,
                    stock.export_quantity,
                    stock.import_quantity,
                    stock.import_by,
                    stock.export_by,
                    stock.last_updated
                    ])
            return response
            dict = {'title':title, 'queryset':queryset, 'form':form}
    return render(request, 'list_history.html', context=dict)

@login_required
def add_items(request):
    title = 'Add Item'
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Saved Successfully')
        return HttpResponseRedirect(reverse('list_items'))
    dict = {'title':title, 'form':form}
    return render(request, 'add_items.html', context=dict)

@login_required
def update_items(request,pk):
    title = 'Update Item'
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully')
            return HttpResponseRedirect(reverse('list_items'))
    dict = {'title':title, 'form':form, 'queryset':queryset}
    return render(request, 'add_items.html', context=dict)

@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Delete Successfully')
        return HttpResponseRedirect(reverse('list_items'))
    return render (request, 'delete_items.html')

@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    dict = { 'queryset':queryset}
    return render(request, 'stock_detail.html', context=dict)

@login_required
def export_items(request,pk):
    queryset = Stock.objects.get(id=pk)
    form = ExportForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.import_quantity = 0
        if instance.quantity - instance.export_quantity>=0:
            instance.quantity -= instance.export_quantity
            instance.export_by = str(request.user)
            messages.success(request, "Export " + str(instance.export_quantity) + " " + str(instance.item_name)+ " Successfully || " + str(instance.quantity)+" " + str(instance.item_name) + "s now left in Store")
            instance.save()
            return redirect('/stock_detail/' +str(instance.id))
        else:
            messages.success(request, 'Product are not enough')
    return render(request, 'add_items.html', context={'title':'Export ' + str(queryset.item_name), 'queryset':queryset, 'form':form, 'username': 'Export By : '+str(request.user) })

@login_required
def import_items(request,pk):
    queryset = Stock.objects.get(id=pk)
    form = ImportForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.export_quantity = 0
        instance.quantity += instance.import_quantity
        instance.save()
        messages.success(request, "Import " + str(instance.import_quantity) + " " + str(instance.item_name)+ " Successfully || " + str(instance.quantity)+ " "+str(instance.item_name)+ "s now in store")
        return redirect('/stock_detail/' +str(instance.id))
    return render(request, 'add_items.html', context={'title': 'Receive '+ str(queryset.item_name), 'queryset':queryset, 'form':form, 'username':'Import By:' +str(request.user)} )

@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Reorder level for ' + str(instance.item_name) + ' is updated to '+ str(instance.reorder_level))
        return HttpResponseRedirect(reverse('list_items'))

    dict = {'instance':queryset, 'form':form}
    return render(request, 'add_items.html', context=dict)

@login_required
def settings(request):
    title = 'Add Category'
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return HttpResponseRedirect(reverse('list_items'))
    return render(request, 'settings.html', context={'title':title, 'form':form})
