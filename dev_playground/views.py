from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

def say_hello(request):
    queryset = Product.objects.values('id','title')
    list(queryset)
    return render(request,'hello.html', {'name': 'Dhanya'})