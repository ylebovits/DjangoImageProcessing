from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {"title": "Home", "image": None}

    if request.method == "POST":
        context["image"] = "/img/sample.bmp"
        for k,v in request.POST.items():
            print(k, v)

    return render(request=request,
              template_name="index.html",
              context=context)
