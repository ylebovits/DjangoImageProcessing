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
            name, ext = file.name.split(".")

            # TODO:
            # modify this to read/write S3 rather than local disk

            tmp_imgPath = default_storage.save(f'{name}.{ext}', ContentFile(file.read()))
            tmp_imgPath = os.path.join(settings.MEDIA_URL, tmp_imgPath)
            imgPath = process_image(tmp_imgPath, upload.cleaned_data["filter"])

            if not imgPath:
                imgPath = None
                context["errors"] = {"error": ["Error processing image"]}

            context["image"] = imgPath

        else:
            context["errors"] = upload.errors

    return render(request=request,
                  template_name="index.html",
                  context=context)


# use PIL to apply 1 or 5 filers to image
def process_image(file_name: str, img_filter: str):
    img = Image.open(file_name)

    try:
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

    except Exception as e:
        return False

    out_file_name = "-out.".join(file_name.split("."))

    img.save(out_file_name)

    os.remove(file_name)  # remove original image copy once it has been processed

    if not s3_upload(out_file_name):
        print("error uploading image")

    return s3_download(out_file_name)


def s3_upload(file_name: str):
     s3 = boto3.resource("s3")

     try:
         with open(file_name, "rb") as file_content:
             s3.Bucket("ylcis4517project1").put_object(Key=file_name, Body=file_content)

         os.remove(file_name)  # once successfully uploaded, remove local copy
         return True

     except Exception as e:
        print(e)
        return False


def s3_download(key: str):
    try:
        s3 = boto3.resource("s3")

        tmp_name = "-s3.".join(key.split("."))
        s3.Object("ylcis4517project1", key).download_file(tmp_name)
        return tmp_name

    except Exception as e:
        print(e)
        return False

