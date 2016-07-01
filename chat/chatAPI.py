import os

class FilesChatManager(object):
    def __init__(self, sender, reciever):
        self.sender = sender
        self.reciever = reciever

        self.file_name = self.get_file_name()
        self.file_path = self.get_file_path()

        self.num_messages_toget = 10

    def get_file_name(self):
        for root, dirs, files in os.walk('./conversations', topdown=False):
            for name in files:
                if name == '{0}_{1}.txt'.format(self.sender,self.reciever) or name == '{1}_{0}.txt'.format(self.sender,self.reciever):
                    file_found = name
                    return file_found
        return None

    def get_file_path(self):
        try:
            basepath = os.path.dirname(__file__)
            path = os.path.join(basepath, '..', 'conversations' , self.file_name)
            return path
        except:
            return None

    def get_messages(self):
        with open(self.file_path, 'r') as file_conversation:
            msgs = file_conversation.read().splitlines()
            msgs_enviar = []

            if len(msgs) > self.num_messages_toget:
                for mensagem in range( len(msgs)-1, len(msgs)-num_de_msgs_get -1, -1):
                    msgs_enviar.append(msgs[mensagem])
            else:
                for mensagem in range( len(msgs)-1, -1, -1):
                    msgs_enviar.append(msgs[mensagem])

            msgs_enviar.reverse()

        return msgs_enviar

    def add_message(self, message):
        with open(self.file_path ,'a+') as file_conversation:
            file_conversation.write(self.sender + ': ' + message + '\n')

    def new_conversation(self, message):
        basepath = os.path.dirname(__file__)
        new_file_name = '{0}_{1}.txt'.format(self.sender, self.reciever)

        new_file_path = os.path.join(basepath, '..', 'conversations' , new_file_name)

        with open(new_file_path ,'a+') as file_conversation:
            file_conversation.write(self.sender + ': ' + message + '\n')
