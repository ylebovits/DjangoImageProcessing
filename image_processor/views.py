import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from image_processor.forms import UploadForm
from PIL import Image, ImageOps, ImageFilter
import boto3


# all steps of processing (upload, filter, display) are done on the home page
def index(request):
    context = {"title": "Home", "form": UploadForm,
               "image": None, "errors": None}

    if request.method == "POST":
        upload = UploadForm(request.POST, request.FILES)

        if upload.is_valid():
            file = upload.cleaned_data["imgFile"]
            ext = file.name.split(".")[1]

            # TODO:
            # modify this to read/write S3 rather than local disk

            tmp_imgPath = default_storage.save(f'tmp.{ext}', ContentFile(file.read()))
            tmp_imgPath = os.path.join(settings.MEDIA_URL, tmp_imgPath)
            imgPath = process_image(tmp_imgPath, upload.cleaned_data["filter"])
            context["image"] = imgPath

        else:
            context["errors"] = upload.errors

    return render(request=request,
                  template_name="index.html",
                  context=context)


# use PIL to apply filters to image
def process_image(file_name: str, img_filter: str):
    img = Image.open(file_name)

    # some issue here that I don't want to fix
    # if img_filter == "sepia":
    #     sepia = []
    #     r, g, b = (239, 224, 185)
    #     for i in range(255):
    #         sepia.extend((r * i / 255, g * i / 255, b * i / 255))
    #     img = img.convert("L")
    #     img.putpalette(sepia)
    #     img = img.convert("RGB")

    if img_filter == "blur":
        img = img.filter(ImageFilter.BLUR)

    if img_filter == "edge":
        img = ImageOps.grayscale(img)
        img = img.filter(ImageFilter.FIND_EDGES)

    if img_filter == "solar":
        img = ImageOps.solarize(img, threshold=80)

    if img_filter == "gray":
        img = ImageOps.grayscale(img)

    if img_filter == "poster":
        img = ImageOps.posterize(img, 3)

    out_file_name = "-out.".join(file_name.split("."))

    img.save(out_file_name)
    s3_upload(out_file_name)
    return out_file_name


def s3_upload(file_name: str):
    s3 = boto3.resource("s3")

    try:
        with open(file_name, "wb") as file_content:
            s3.Bucket("ylcis4517project1").put_object(Key=file_name,
                                                      Body=file_content)
        return "success"
    except Exception as e:
        return e



