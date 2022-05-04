import sys

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
# sys.path.append("C:/Users/Matko/Desktop/Projekti/lil GUESSR")
import main

# Create your views here.
@csrf_exempt
def index(request):
    print(request.FILES)
    # my_file = request.FILES['0.jpg']
    # filename = my_file.read()
    # print("aksfbasdklflasdbffffffffffffffffffffffffadn", request.FILES['0.jpg'].temporary_file_path())
    return JsonResponse(main.predict_coords(request))
