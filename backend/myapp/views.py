import sys

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

sys.path.append("C:/Users/Ana/Desktop/Ana/Dodatno/Lumen/Lumen")
#sys.path.append("C:/Users/Matko/Desktop/Projekti/lil GUESSR")
import main

# Create your views here.
@csrf_exempt
def index(request):
    return JsonResponse(main.dummy_fun())
