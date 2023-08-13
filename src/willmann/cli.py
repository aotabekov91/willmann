import json

from plug import Plug

from .main import Willmann

class WillmannCLI(Plug):

    def setConnection(self): pass

    def setParser(self):

        super().setParser()

        self.subparser=self.parser.add_subparsers(dest='main')

        self.subparser.add_parser('quit')
        self.action_parser=self.subparser.add_parser('action')

        self.action_parser.add_argument('-m', '--mode')
        self.action_parser.add_argument('-c', '--command')
        self.action_parser.add_argument('-p', '--port', type=int)

    def setSocket(self, kind='main'): 

        if kind=='main':
            self.socket = self.getConnection(kind='REQ')
            self.socket.connect(f'tcp://localhost:{self.port}')
        elif kind=='port':
            self.socket = self.getConnection(kind='PUSH')
            self.port=self.socket.bind_to_random_port(
                    'tcp://*', 
                    min_port=10000, 
                    max_port=16000)

    def portAction(self, port, action, request={}):

        self.setSocket(kind='port')
        socket = self.getConnection(kind='PUSH')
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
        elif args.main=='quit':
            self.appAction('quit')

def run():

   app=WillmannCLI()
   app.run()
