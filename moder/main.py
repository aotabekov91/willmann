import sys
import zmq

from plugin import Plug

class Moder(Plug):

    def __init__(self):
        super(Moder, self).__init__()

        self.modes={}
        self.data={}
        self.sockets={}

        self.modes_path=None
        self.current_mode=None
        self.previous_mode=None
        self.last_command=None
        self.private_mode=False

    def setMode(self, mode_name):
        if mode_name!='CurrentMode':
            self.previous_mode=self.current_mode
            self.current_mode=mode_name

    def setListener(self):
        super().setListener(kind=zmq.REP)

    def respond(self, r):
        if not r['command'] in ['storeData', 'accessStoreData', 'currentMode']: print(r)
        try:

            if r['command']=='currentMode':
                msg={'status':'ok', 
                     'currentMode':self.current_mode,
                     'lastCommand': self.last_command,
                     }
            elif r['command']=='previousMode':
                msg={'status':'ok', 'previousMode':self.previous_mode}
            elif r['command']=='getModes':
                msg={'status':'ok', 'modes':self.modes}
            elif r['command']=='setMode':
                self.setMode(r.get('mode_name'))
                msg={'status':'ok', 'currentMode':self.current_mode}
            elif r['command']=='getAllModes':
                msg={'status':'ok', 'allModes':self.modes}
            elif r['command']=='setModeAction':
                mode_name=r['mode_name']
                self.setMode(mode_name)
                mode_action=r['mode_action']
                intent_data=r.get('intent_data', {})
                slot_names=r.get('slot_names', {})
                self.act(mode_name, mode_action, slot_names, intent_data)
                msg={'status':'ok', 'action':'setMode', 'info': r}
            elif r['command']=='notify':
                self.act('NotifyMode', 'notify', r, r)   
                msg={'status':'ok', 'action':'setListener'}
            elif r['command']=='storeData':
                mode_store=self.data.get(r['mode_name'])
                mode_store[r['data_name']]=r['data']
                msg={'status':'ok', 'action':'storeData'}
            elif r['command']=='accessStoreData':
                mode_store=self.data.get(r['mode_name'], {})
                data=mode_store.get(r['data_name'], {})
                msg={'status':'ok', 'action':'accessStoreData', 'data':data}
            elif r['command']=='registerMode':
                self.modes[r['mode_name']]=r
                self.data[r['mode_name']]={}
                self.createSocket(r)
                msg={'status':'ok', 'action': 'registeredMode', 'info': r['mode_name']}
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

        self.socket.send_json(msg)

    def createSocket(self, r):
        socket=zmq.Context().socket(zmq.PUSH)
        socket.connect(f'tcp://localhost:{r["port"]}')
        self.sockets[r['mode_name']]=socket

    def act(self, mode_name, command_name, slot_names={}, intent_data={}):
        if mode_name=='CurrentMode':
            mode_name=self.current_mode
        if mode_name in self.modes:
            self.last_command=command_name.split('_')[-1]
            socket=self.sockets[mode_name]
            socket.send_json({'command': command_name,
                              'slot_names':slot_names,
                              'intent_data':intent_data,
                              })

    def run(self):
        self.running=True
        while self.running:
            self.respond(self.socket.recv_json())

    def exit(self, close_modes=True):
        self.running=False

if __name__=='__main__':
    app=Moder()
    app.run()
