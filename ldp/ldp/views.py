from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404

from actstream.models import model_stream
from actstream.views import actor

def home(request):
    return render(request, "index.html", {'activities': model_stream(get_user_model())[:10] })

def skater_activities(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    content_type_id = ContentType.objects.get_for_model(user).pk

    return actor(request, content_type_id, user.pk)