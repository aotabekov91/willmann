import os
import sys
import zmq
import shutil
import inspect
import importlib
import multiprocessing
from pathlib import Path

from plug import Plug

class Willmann(Plug):

    def __init__(self):

        super(Willmann, self).__init__()

        self.modes={}
        self.sockets={}
        self.mode_runner=[]

        self.createConfig()

    def createConfig(self):

        super().createConfig('~/.config/willmann')
        self.modes_path=self.config_folder/'modes'

        if not os.path.exists(
                os.path.expanduser('~/.config/willmann/modes')):

            self.modes_path.mkdir(parents=True, exist_ok=True)
            path=Path(os.path.abspath(inspect.getfile(self.__class__)))
            shutil.copytree(
                    str(path.parent/'modes'), 
                    str(self.modes_path), 
                    dirs_exist_ok=True)

        if not os.path.exists(self.config_folder/'config.ini'):
            shutil.copy(
                    str(path.parent/'config.ini'), 
                    str(self.config_folder/'config.ini'))

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
                mode=mode_class(parent_port=willmann_port)
                mode.run()

            t=multiprocessing.Process(
                    target=start, 
                    args=(mode_class, willmann_port))
            t.deamon=True
            t.start()

        def load(mode):

            mode=importlib.import_module(mode)

            if hasattr(mode, 'get_mode_class'):
                mode_class=mode.get_mode_class()
                run_in_background(mode_class, self.port)

        self.modes_path=self.config_folder/'modes'

        if self.modes_path:

            sys.path=[str(self.modes_path)]+sys.path
            for mode in os.listdir(self.modes_path): 

                # try:

                # print(mode, sys.path)
                load(mode)

                # except:
                #     print(f'Willmann: Could not load mode {mode}')

    def setConnection(self): super().setConnection(kind=zmq.REP)

    def handle(self, request):

        print(f'{self.name} received: ', request)

        try:

            command=request.get('command' , None)

            if command=='getModes':
                msg={'status':'ok', 'modes':self.modes}
            elif command=='quit':
                msg={'status':'ok', 'info':'exiting'}
                self.exit()
            elif command=='setModeAction':
                mode=request['mode']
                action=request.get('action', None)
                if action:
                    self.act(mode, action, request)
                    msg={'status':'ok', 'action':'setModeAction', 'info': request}
                else:
                    msg={'status':'nok', 'action':'setModeAction', 'info': request}
            elif command=='register':
                mode=request['mode']
                port=request['port']
                self.modes[mode]=request
                self.createSocket(mode, port)
                self.act('Moder', 'update', {'action':'update', 'modes':self.modes})
                msg={'status':'ok', 'action': 'registeredMode', 'info': request['mode']}
            else:
                msg={'status':'nok', 'info':'request not understood'}

        except:

           err_type, error, traceback = sys.exc_info()
           msg={'status':'nok',
                 'info': 'an error has occured',
                 'error': str(error),
                 'agent': self.__class__.__name__}
        
        return msg

    def createSocket(self, mode, port):

        socket=zmq.Context().socket(zmq.PUSH)
        socket.connect(f'tcp://localhost:{port}')
        self.sockets[mode]=socket

    def act(self, mode, action, request={}): 

        socket=self.sockets.get(mode, None)
        if socket: 
            request['action']=action
            socket.send_json(request)

    def run(self):

        self.loadModes()
        super().run(answer=True)

    def exit(self):

        for mode in self.modes: self.act(mode, 'exit')
        super().exit()

def run():

    app=Willmann()
    app.run()
