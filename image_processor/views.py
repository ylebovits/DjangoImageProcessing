from django.shortcuts import render
from image_processor.forms import UploadForm


def index(request):
    context = {"title": "Home", "form": UploadForm,
               "image": None, "errors": None}

    if request.method == "POST":
        upload = UploadForm(request.POST, request.FILES)

        if upload.is_valid():
            context["image"] = "/img/sample.bmp"
            print("good!")

        else:
            context["errors"] = upload.errors
            print(context["errors"])

    return render(request=request,
                  template_name="index.html",
                  context=context)
