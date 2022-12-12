from django.shortcuts import render
from django.http import HttpResponse

def home(requests):
   return render(requests,'home.html')