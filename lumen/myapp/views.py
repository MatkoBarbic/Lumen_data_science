from django.shortcuts import render
from django.http import HttpResponse
import sys
sys.path.append("C:/Users/Ana/Desktop/Ana/Dodatno/Lumen/backend")
import main

# Create your views here.
def index(request):
    return HttpResponse(main.dummy_fun())
