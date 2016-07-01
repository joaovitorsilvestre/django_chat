import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from accounts.models import Usuario
from .chatAPI import FilesChatManager

def Index(request):
    if request.user.is_active:
        return render(request, 'chat/index.html', {'usuario': request.user.name})

    return HttpResponseRedirect('/accounts/login')

def Users_on(request):
    users_on_found = {'on': []}

    for user in Usuario.objects.filter(online=True):
        if user != request.user:
            users_on_found['on'].append(user.username)

    return JsonResponse(users_on_found)

def Messages_get(request, user):
    manager = FilesChatManager(sender=request.user, reciever=user)

    if manager.file_name:
        messages =  manager.get_messages()
        return HttpResponse(json.dumps(messages), content_type='application/json')
    else:
        return HttpResponse(json.dumps(['Inicie uma nova conversa.']))

    return HttpResponse('fail')

def Messages_send(request):
    sender = request.user.username
    receiver = request.POST.get('toUser')
    message = request.POST.get('text')

    manager = FilesChatManager(sender=sender, reciever=receiver)

    if manager.file_name:
        manager.add_message(message=message)
        return HttpResponse('sucsess')
    else:
        manager.new_conversation(message=message)
        return HttpResponse('sucsess')

    return HttpResponse('fail')
