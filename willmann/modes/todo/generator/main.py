import os
import zmq
import json
import random
import hashlib
import playsound

from plugin.utils import register
from plugin.widget import InputListStack

from willmann import GenericMode, command

class GeneratorMode(GenericMode):

    def __init__(self, port=None, parent_port=None, config=None):
        super(GeneratorMode, self).__init__(
                 port=port, 
                 parent_port=parent_port, 
                 config=config)

        self.setUI()
        self.setMode('sound')

    def setUI(self):

        self.ui=InputListStack()
        self.ui.main.input.setLabel('Generate')
        self.ui.main.returnPressed.connect(self.confirm)

        self.ui.installEventFilter(self)

    def setSettings(self):
        super().setSettings()
        self.quotes= json.load(open(self.quotes_path))
        self.jokes= json.load(open(self.jokes_path))

    def setConnection(self):
        super().setConnection()
        if self.generator_port:
            self.gsocket=zmq.Context().socket(zmq.PUSH)
            self.gsocket.connect(f'tcp://localhost:{self.generator_port}')

    def setMode(self, mode):
        self.mode=mode
        self.ui.main.input.setLabel(f'Generate {self.mode}')

    @register('s')
    def soundMode(self):
        self.setMode('sound')

    @register('i')
    def imageMode(self): 
        self.setMode('image')

    @register('j')
    def jokeMode(self):
        self.ui.main.input.clear()
        self.setMode('joke')
        self.confirm()

    @register('x')
    def quoteMode(self):
        self.ui.main.input.clear()
        self.setMode('quote')
        self.confirm()

    def confirm(self):
        if self.mode=='sound':
            path=self.getPath(kind='sound')
            if path:
                playsound.playsound(path, block=False)
        elif self.mode=='image':
            path=self.getPath(kind='image')
            if path:
                dlist=[{'up':self.ui.main.input.text()(), 'icon':path}]
                self.ui.main.setList(dlist)
                self.ui.show()
        elif self.mode=='quote':
            quote=self.quotes[random.randint(0, len(self.quotes))]
            dlist=[{'up':quote['text'], 'down':quote['author']}]
            self.ui.main.setList(dlist)
            self.ui.show()
        elif self.mode=='joke':
            joke=self.jokes[random.randint(0, len(self.jokes))]
            dlist=[{'up':joke['joke'], 'down':joke['name']}]
            self.ui.main.setList(dlist)
            self.ui.show()

    def getPath(self, kind):
        if kind=='sound':
            ext='wav'
        elif kind=='image':
            ext='jpg'
        text=self.ui.main.input.text()
        path=f'/tmp/{hashlib.md5(text.encode()).hexdigest()}.{ext}'
        if os.path.isfile(path):
            return path
        self.gsocket.send_json({'kind':kind, 'text':text, 'path':path})
        i=0
        while not os.path.isfile(path) or i<300:
            i+=1
        if os.path.isfile(path):
            return path

    @register('c')
    def toggleCommands(self):
        self.ui.toggleCommands()

    def toggle(self):
        if not self.ui.isVisible():
            self.activate()
        else:
            self.deactivate()

if __name__=='__main__':
    app=GeneratorMode(port=33333)
    app.toggle()
    app.run()
