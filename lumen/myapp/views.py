import sys

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

sys.path.append("C:/Users/Ana/Desktop/Ana/Dodatno/Lumen/Lumen")
import main

# Create your views here.
@csrf_exempt
def index(request):
    return HttpResponse(main.dummy_fun())
