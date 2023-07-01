import os
import sys
import zmq
import inspect
import importlib
import multiprocessing

from tendo import singleton
from plugin.plug import Plug

class Willmann(Plug):

    def __init__(self):

        super(Willmann, self).__init__()

        self.data={}
        self.modes={}
        self.sockets={}
        self.mode_runner=[]

        self.current=None
        self.previous=None
        self.last_command=None

    def setSettings(self):

        super().setSettings()

        self.modes_path=None
        file_path=os.path.abspath(inspect.getfile(self.__class__))
        folder_path=os.path.dirname(file_path).replace('\\', '/')
        modes_path=os.path.join(folder_path, 'modes')
        if os.path.exists(modes_path): 
            self.modes_path=modes_path

    def loadModes(self):

        def run_in_background(mode_class, willmann_port):

            def start(mode_class, willmann_port):

                try:
                    mode=mode_class(parent_port=willmann_port)
                    mode.run()
                except:
                    print(mode_class, 'Error')
                    raise

            t=multiprocessing.Process(
                    target=start, 
                    args=(mode_class, willmann_port))
            t.deamon=True
            t.start()

        if self.modes_path:

            sys.path=[self.modes_path]+sys.path
            for mode in os.listdir(self.modes_path):
                plugin=importlib.import_module(mode)
                if mode in self.modes_include:
                    if hasattr(plugin, 'get_mode'):
                        mode_class=plugin.get_mode()
                        run_in_background(mode_class, self.port)

    def setMode(self, mode):

        if mode!='currentMode':
            self.previous=self.current
            self.current=mode

    def setListener(self):

        super().setListener(kind=zmq.REP)

    def handle(self, r):

        if not r['command'] in ['storeData', 'accessData', 'currentMode']: print(r)

        try:

            if r['command']=='currentMode':
                msg={'status':'ok', 
                     'currentMode':self.current,
                     'lastCommand': self.last_command,
                     }
            elif r['command']=='previousMode':
                msg={'status':'ok', 'previousMode':self.previous}
            elif r['command']=='getModes':
                msg={'status':'ok', 'modes':self.modes}
            elif r['command']=='setMode':
                self.setMode(r.get('mode'))
                msg={'status':'ok', 'currentMode':self.current}
            elif r['command']=='getAllModes':
                msg={'status':'ok', 'allModes':self.modes}
            elif r['command']=='setModeAction':
                mode=r['mode']
                action=r['action']
                slots=r.get('slots', {})
                self.setMode(mode)
                self.act(mode, action, slots)
                msg={'status':'ok', 'action':'setModeAction', 'info': r}
            elif r['command']=='notify':
                self.act('NotifyMode', 'notify', r)
                msg={'status':'ok', 'action':'setListener'}
            elif r['command']=='storeData':
                mode_store=self.data.get(r['mode'])
                mode_store[r['name']]=r['data']
                msg={'status':'ok', 'action':'storeData'}
            elif r['command']=='accessData':
                mode_store=self.data.get(r['mode'], {})
                data=mode_store.get(r['name'], {})
                msg={'status':'ok', 'action':'accessData', 'data':data}
            elif r['command']=='register':
                self.modes[r['mode']]=r
                self.data[r['mode']]={}
                self.createSocket(r)
                self.act('Moder', 'Moder_update', {'modes':self.modes})
                msg={'status':'ok', 'action': 'registeredMode', 'info': r['mode']}
            elif r['command']=='exit':
                msg={'status':'ok', 'info':'exiting'}
                self.exit()
            else:
                msg={'status':'nok', 'info':'request not understood'}

        except:

           err_type, error, traceback = sys.exc_info()
           msg={'status':'nok',
                 'info': 'an error has occured',
                 'error': str(error),
                 'agent': self.__class__.__name__}
        
        return msg

    def createSocket(self, r):

        socket=zmq.Context().socket(zmq.PUSH)
        socket.connect(f'tcp://localhost:{r["port"]}')
        self.sockets[r['mode']]=socket

    def act(self, mode, action, slots={}): 

        if mode=='currentMode': mode=self.current
        if mode in self.modes:
            self.last_command=action.split('_')[-1]
            socket=self.sockets.get(mode, None)
            if socket: socket.send_json({'action': action, 'slots':slots})

    def run(self):

        singleton.SingleInstance()
        self.loadModes()
        super().run()

    def exit(self):

        for mode in self.modes: self.act(mode, 'exit')
        super().exit()
