from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import Usuario
from django.views.decorators.csrf import csrf_exempt
import json, os


def Chat(request):
    usuario = request.user

    return render(request, 'chat/chat.html', {'usuario': usuario})



# funções abaixo são para retornar json para pedidos feitos pelo ajax
def Users_on(request):
    users_on = []
    for u in Usuario.objects.all():
        if u.online == True:
            if u.username != request.user.username:
                users_on.append(u.username)

    json_data = json.dumps(users_on)

    return HttpResponse(json_data)

@csrf_exempt
def Send_message(request):
    if request.method == 'POST':
        de = request.POST['de']
        para = request.POST['para']
        message = request.POST['message']

        for root, dirs, files in os.walk("./conversations", topdown=False):
            for name in files:
                if name == '{0}_{1}.txt'.format(de,para) or name == '{0}_{1}.txt'.format(para,de):
                    file_found = name
                else:
                    file_found = None

        if file_found != None:
            basepath = os.path.dirname(__file__)
            path = os.path.join(basepath, '..', 'conversations' , file_found)

            with open(path ,'a+') as conversation:
                conversation.write(de + '--' + message + '\n')
                return HttpResponse('sucsess')
        else:
            basepath = os.path.dirname(__file__)
            path = os.path.join(basepath, '..', 'conversations' , '{0}_{1}.txt'.format(de,para))

            with open(path ,'a+') as conversation:
                conversation.write(de + '--' + message + '\n')
                return HttpResponse('sucsess')

    return HttpResponse('fail em enviar a menssagem')

@csrf_exempt
def Get_message(request):
    if request.method == 'POST':
        de = request.POST['de']
        para = request.POST['para']

        for root, dirs, files in os.walk("./conversations", topdown=False):
            for name in files:
                if name == '{0}_{1}.txt'.format(de,para) or name == '{0}_{1}.txt'.format(para,de):
                    file_found = name
                else:
                    file_found = None

        if file_found != None:
            basepath = os.path.dirname(__file__)
            path = os.path.join(basepath, '..', 'conversations' , file_found)

            with open(path, 'r') as get_conversation:
                msgs = get_conversation.read().splitlines()
                msgs_enviar = []

                num_de_msgs_get = 5
                if len(msgs) > num_de_msgs_get:
                    for mensagem in range( len(msgs)-1, len(msgs)-num_de_msgs_get -1, -1):
                        msgs_enviar.append(msgs[mensagem])
                else:
                    for mensagem in range( len(msgs)-1, 0, -1):
                        msgs_enviar.append(msgs[mensagem])

            msgs_enviar.reverse()
            return HttpResponse(json.dumps(msgs_enviar), content_type='application/json')

        return HttpResponse(json.dumps('nenhuma msg encontrada'))

    return HttpResponse('fail em pegar as mensagen')
