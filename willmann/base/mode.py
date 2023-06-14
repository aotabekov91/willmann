import os
import sys
import zmq
import time
import inspect
from os.path import abspath

from PyQt5.QtCore import QEvent

from plugin import AppPlug

class Mode(AppPlug):

    def __init__(self, 

                 name=None, 
                 port=None, 
                 parent_port=None, 
                 config=None,
                 window_classes='all',
                 app_name='own_floating',
                 leader=None,
                 ):

        self.parent_port=parent_port
        self.window_classes=window_classes

        super(Mode, self).__init__(
                name=name, port=port, config=config, leader=leader,  app_name=app_name)

        self.register()

    def get_mode_folder(self):

        file_path=os.path.abspath(inspect.getfile(self.__class__))
        return os.path.dirname(file_path).replace('\\', '/')

    def register(self):

        if self.parent_port:
            self.parent_socket.send_json({
                'command': 'register',
                'mode':self.__class__.__name__,
                'keyword':self.name,
                'port': self.port,
                'window_classes': self.window_classes})
            respond=self.parent_socket.recv_json()
            print(respond)

    def handle(self, request):

        print(f'{self.__class__.__name__} received: {request}')

        action=request['action'].rsplit('_', 1)
        mode, command=action[0], action[-1]
        func=getattr(self, command, False)
        if not func and hasattr(self, 'ui'): func=getattr(self.ui, command, None)
        if func:
            if 'request' in inspect.signature(func).parameters:
                func(request)
            else:
                func()
            msg=f"{self.__class__.__name__}: handled request"
        elif not mode in [self.__class__.__name__, 'CurrentMode']:
            if self.parent_port:
                self.parent_socket.send_json(
                        {'command':'setModeAction',
                         'mode':mode,
                         'action': request['action'],
                         'slots': request.get('slots', {}),
                         }
                        )
                respond=self.parent_socket.recv_json()
                msg=f'{self.__class__.__name__}: {mode} {request["action"]}'
            else:
                msg=f'{self.__class__.__name__}: {mode} no parent to redirect'
        else:
            msg=f'{self.__class__.__name__}: not understood'

        print(msg)

    def setConnection(self):

        socket=super().setConnection(exit=False)
        if self.parent_port:
            self.parent_socket=zmq.Context().socket(zmq.REQ)
            self.parent_socket.connect(f'tcp://localhost:{self.parent_port}')
        if socket:
            socket.send_json({'command':'setParentPort', 'parent_port':self.parent_port})
            sys.exit()

    def setParentPort(self, request):

        self.parent_port=request['parent_port']
        self.register()

    def activateCommandMode(self):

        self.ui.show(self.ui.commands)

    def deactivateCommandMode(self): 

        self.ui.show(self.ui.previous)

    def eventFilter(self, widget, event):

        handled=False
        if hasattr(self, 'ui') and hasattr(self.ui, 'commands'):
            if event.type()==QEvent.KeyPress:
                if event.text() in self.leader and not self.leader_activated:
                    self.leader_activated=True
                    self.activateCommandMode()
                elif event.text() in self.leader and self.leader_activated:
                    self.leader_activated=False
                    self.deactivateCommandMode()
                else:
                    return widget.event(event)
                handled=True
        if handled:
            return True
        else:
            return super().eventFilter(widget, event)

    def deactivate(self):
        self.hide()

    def activate(self):
        if hasattr(self, 'ui'): self.ui.show()
