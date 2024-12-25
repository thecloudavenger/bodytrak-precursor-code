from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

def say_hello(request):
    #try:
    #     send_mail('subject','message','thecloudavenger@gmail.com',['thecloudavenger@gmail.com'])

    #     mail_admins('subject','message',html_message='message')
    # except BadHeaderError:
    #     pass
    return render(request,'hello.html', {'name': 'Dhanya'})