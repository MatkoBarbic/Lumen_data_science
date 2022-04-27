import sys

from django.http import HttpResponse

sys.path.append("C:/Users/Ana/Desktop/Ana/Dodatno/Lumen/Lumen")
import main

# Create your views here.
def index(request):
    return HttpResponse(main.dummy_fun())
