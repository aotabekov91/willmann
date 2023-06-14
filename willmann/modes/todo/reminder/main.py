import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.app.mode import AppMode

from plugin.app import register
from plugin.widget import CommandsStackWindow, MessageWidget 

class NotifyMode(AppMode):

    def __init__(self, port=None, parent_port=None, config=None):

        super(NotifyMode, self).__init__(
                 port=port, 
                 parent_port=parent_port, 
                 config=config)

        self.setUI()

    def setUI(self):

        self.window=CommandsStackWindow(MessageWidget(), 'OpenAI - own_floating')
        self.ui=self.window.stack
        self.ui.main.hideWanted.connect(self.hide)
        self.ui.installEventFilter(self)

    def hide(self):

        self.window.hide()

    def show(self):

        self.window.show()
        self.ui.main.setMinimumWidth(self.window.size().width())
        self.ui.showMainWidget()

    @register('h')
    def toggleCommands(self):

        self.ui.toggleCommands()

    @register('q')
    def quit(self):

        super().quit()

    def alert(self, request):

        self.show()
        slot_names=request['slot_names']
        mode_name=slot_names.get('mode_name', self.__class__.__name__)
        text=slot_names.get('text', '')
        detail=slot_names.get('detail', '')
        timeout=slot_names.get('timeout', 5000)
        self.ui.main.setTitle(mode_name)
        self.ui.main.setInformation(text)
        self.ui.main.setDetail(detail)
        self.ui.main.setTimer(timeout)

if __name__=='__main__':
    app=NotifyMode(port=33333)
    app.alert({'slot_names':{'text':'test', 'detail': 'really?', 'timeout':10000}})
    app.run()
