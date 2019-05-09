from django.http import HttpResponse


def index(request):
    print("request", request.__dict__)
    return HttpResponse("Hello, world. <br>This was the request : <pre>{}</pre>".format(request))
