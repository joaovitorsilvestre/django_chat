from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import Usuario
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json, os


def Chat(request):
    usuario = request.user
    URL_CHAT = getattr(settings, "URL_CHAT", "/chat/") ## ultimo valor é para caso não tenha sido definida pelo user, então é o default

    return render(request, 'chat/chat.html', {'usuario': usuario, 'URL_CHAT': URL_CHAT})



# funções abaixo são para retornar json para pedidos feitos pelo ajax
def Users_on(request):

    from django.contrib.auth import get_user_model
    user_model = get_user_model()

    try:
        users_on = []
        for u in user_model.objects.all():
            if u.online == True:
                if u.username != request.user.username:
                    users_on.append(u.username)

    except ValueError:
        print('Modelo de user não cadastrado, todos os users encontrados apareceram online.', ValueError)
        users_on = []
        for u in user_model.objects.all():
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
                    break
                else:
                    file_found = None

        if file_found != None:
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
            iniciar_conversa = ['Inicie uma nova conversa']
            return HttpResponse(json.dumps(iniciar_conversa), content_type='application/json')

    return HttpResponse('fail em pegar as mensagen')
