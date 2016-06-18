from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json, os
from accounts.models import Usuario

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
    de = request.user.username
    para = user

    file_found = None

    for root, dirs, files in os.walk('./conversations', topdown=False):
        for name in files:
            if name == '{0}_{1}.txt'.format(de,para) or name == '{1}_{0}.txt'.format(de,para):
                file_found = name
                break

    if file_found:
        basepath = os.path.dirname(__file__)
        path = os.path.join(basepath, '..', 'conversations' , file_found)

        with open(path, 'r') as get_conversation:
            msgs = get_conversation.read().splitlines()
            msgs_enviar = []

            num_de_msgs_get = 10
            if len(msgs) > num_de_msgs_get:
                for mensagem in range( len(msgs)-1, len(msgs)-num_de_msgs_get -1, -1):
                    msgs_enviar.append(msgs[mensagem])
            else:
                for mensagem in range( len(msgs)-1, -1, -1):
                    msgs_enviar.append(msgs[mensagem])

            msgs_enviar.reverse()
            return HttpResponse(json.dumps(msgs_enviar), content_type='application/json')
    else:
        return HttpResponse(json.dumps(['Inicie uma nova conversa.']))

    return HttpResponse('fail')

def Messages_send(request):
    if request.method == 'POST':
        de = request.user.username
        message = request.POST.get('text')
        para = request.POST.get('toUser')

        file_found = None
        for root, dirs, files in os.walk("./conversations", topdown=False):
            for name in files:
                if name == '{0}_{1}.txt'.format(de,para) or name == '{0}_{1}.txt'.format(para,de):
                    file_found = name
                    break

        if file_found:
            basepath = os.path.dirname(__file__)
            path = os.path.join(basepath, '..', 'conversations' , file_found)

            with open(path ,'a+') as conversation:
                conversation.write(de + ': ' + message + '\n')
                return HttpResponse('sucsess')
        else:
            basepath = os.path.dirname(__file__)
            path = os.path.join(basepath, '..', 'conversations' , '{0}_{1}.txt'.format(de,para))

            with open(path ,'a+') as conversation:
                conversation.write(de + ': ' + message + '\n')
                return HttpResponse('sucsess')

    return HttpResponse('fail')

def Send_message(request):
    if request.method == 'POST':
        de = request.POST['de']
        para = request.POST['para']
        message = request.POST['message']

        for root, dirs, files in os.walk("./conversations", topdown=False):
            for name in files:
                if name == '{0}_{1}.txt'.format(de,para) or name == '{0}_{1}.txt'.format(para,de):
                    file_found = name
                    break
                else:
                    file_found = None

        if file_found != None:
            basepath = os.path.dirname(__file__)
            path = os.path.join(basepath, '..', 'conversations' , file_found)

            with open(path ,'a+') as conversation:
                conversation.write(de + ': ' + message + '\n')
                return HttpResponse('sucsess')

        else:
            basepath = os.path.dirname(__file__)
            path = os.path.join(basepath, '..', 'conversations' , '{0}_{1}.txt'.format(de,para))

            with open(path ,'a+') as conversation:
                conversation.write(de + ': ' + message + '\n')
                return HttpResponse('sucsess')
