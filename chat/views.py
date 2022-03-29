from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def course_chat_room(request, course_id):
    try:
        # pobranie kursu zgodnym z id kursu, do ktorego dolaczyl uzytkownik
        course = request.user.coursed_joined.get(id=course_id)
    except:
        # nie jest uczestnikiem lub kurs nie istnieje
        return HttpResponseForbidden()
    return render(request, 'chat/room.html', {'course': course})
