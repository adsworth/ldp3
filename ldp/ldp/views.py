from django.shortcuts import render

from actstream.models import model_stream


def home(request):
    return render(request, "index.html", {'activities': model_stream(request.user)[:10] })