import zmq
import json
import argparse

from plugin.plug import Plug

from .main import Willmann

class WillmannCLI(Plug):

    def setConnection(self): pass

    def setSettings(self):

        super().setSettings()

        self.parser=argparse.ArgumentParser()

        self.subparser=self.parser.add_subparsers(dest='main')

        self.subparser.add_parser('run')
        self.subparser.add_parser('quit')
        self.subparser.add_parser('restart')
        self.action_parser=self.subparser.add_parser('action')

        self.action_parser.add_argument('-m', '--mode')
        self.action_parser.add_argument('-c', '--command')
        self.action_parser.add_argument('-p', '--port', type=int)

    def setSocket(self, kind='main'): 

        if kind=='main':
            self.socket = zmq.Context().socket(zmq.REQ)
            self.socket.connect(f'tcp://localhost:{self.port}')
        elif kind=='port':
            self.socket=zmq.Context().socket(zmq.PUSH)
            self.port=self.socket.bind_to_random_port(
                    'tcp://*', 
                    min_port=10000, 
                    max_port=16000)

    def portAction(self, port, action, request={}):

        self.setSocket(kind='port')
        socket = zmq.Context().socket(zmq.PUSH)
        socket.connect(f'tcp://localhost:{port}')
        request['action']=action
        socket.send_json(request)

    def modeAction(self, mode, action, request={}):

        self.setSocket(kind='main')
        request['action']=action
        request['command']='setModeAction' 
        request['mode']=mode
        self.socket.send_json(request)

        response=self.socket.recv_json()
        json_object = json.dumps(response, indent = 4) 
        print(json_object)

    def appAction(self, command=None, request={}):

        self.setSocket(kind='main')
        if command: request['command']=command

        self.socket.send_json(request)

        response=self.socket.recv_json()
        json_object = json.dumps(response, indent = 4) 
        print(json_object)

    def runApp(self):

        app=Willmann()
        self.setSocket(kind='main')

        if app.socket:
            app.run()
        else:
            print('An instance of Willmann is already running')

    # TODO: finish & add socket polling in quit

    def run(self):

        args, unknown = self.parser.parse_known_args()

        request={}
        for i in range(0, len(unknown), 2):
            request[unknown[i][2:]]=unknown[i+1]

        if args.main=='action':
            if args.port:
                self.portAction(args.port, args.command, request)
            elif args.mode:
                self.modeAction(args.mode, args.command, request)
            else:
                self.appAction(args.command, request=request)
        elif args.main=='run':
            self.runApp()
        elif args.main=='quit':
            self.appAction('quit')
        elif args.main=='restart':
            self.appAction('restart')

if __name__=='__main__':

    cli = WillmannCLI()
    cli.run()
