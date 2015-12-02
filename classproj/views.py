from django.http import HttpResponse

def index(request):
    return HttpReponse("Hello, world. You're at the first page!")
