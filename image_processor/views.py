from django.shortcuts import render
from image_processor.forms import UploadForm

def index(request):
    context = {"title": "Home", "image": None}

    if request.method == "POST":
        form = UploadForm(request.POST)
        print(form.filter)
        if form.is_valid():
            context["image"] = "/img/sample.bmp"
            print("good!")
        else:
            print("bad form!")

    return render(request=request,
                  template_name="index.html",
                  context=context)
