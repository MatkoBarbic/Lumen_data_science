import sys

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
sys.path.append("..")
import main

# Create your views here.
@csrf_exempt
def index(request):
    return JsonResponse(main.predict_coords(request))
