import os
import sys
import zmq

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.utils import register
from plugin.widget import InputListStack

from willmann import GenericMode, command

class ChangerMode(GenericMode):

    def __init__(self, port=None, parent_port=None, config=None):

        super(ChangerMode, self).__init__(
                 port=port, 
                 parent_port=parent_port, 
                 config=config)

        self.setUI()

    def setUI(self):

        self.ui=InputListStack()
        self.ui.main.input.setLabel('Mode')
        self.ui.main.returnPressed.connect(self.confirm)
        self.ui.installEventFilter(self)

    def toggle(self): 

        if not self.ui.isVisible(): 
            self.activate()
        else:
            self.deactivate()

    def deactivate(self):

        self.ui.hide()

    def activate(self):

        dlist=self.get_modes()
        self.ui.main.setList(dlist)
        self.ui.show()

    def confirm(self):

        item=self.ui.main.list.currentItem()
        if item and self.parent_port:
            self.ui.hide()
            self.ui.main.clear()
            mode_name=item.itemData.get('id')
            print(mode_name)
            self.parent_socket.send_json(
                    {'command': 'setModeAction',
                     'mode_name':mode_name,
                     'mode_action': 'activate',
                     })
            respond=self.parent_socket.recv_json()

    def get_modes(self):

        if self.parent_port:
            # poller=zmq.Poller()
            # poller.register(self.parent_socket, flags=zmq.POLLIN)
            self.parent_socket.send_json({'command': 'getModes'})
            # sock=poller.poll(timeout=1000)
            # data=[]
            # if len(sock)>0 and sock[0][0]==self.parent_socket:
            respond=self.parent_socket.recv_json()#zmq.NOBLOCK)
            data=self.get_data(respond)
            # poller.unregister(self.parent_socket)
            return data

    def get_data(self, respond):

        modes=respond.get('modes', [])
        data=[]
        for name, mode in modes.items():
            data+=[{'up':name, 'id':name}]
        return data

if __name__=='__main__':
    app=ChangerMode(port=33332, parent_port=9999)
    app.toggle()
    app.run()
