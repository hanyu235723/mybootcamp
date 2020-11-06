from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
import json

@login_required
def room(request, room_name):
    return render(request, 'chat/Room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'user_name' :mark_safe(json.dumps(request.user.first_name))
    })
