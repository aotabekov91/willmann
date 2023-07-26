import zmq
import argparse

from plugin.plug import Plug

from .main import Willmann

class WillmannCLI(Plug):

    def setSettings(self):

        super().setSettings()

        self.parser=argparse.ArgumentParser()

        self.subparser=self.parser.add_subparsers(dest='command')

        self.subparser.add_parser('run')
        self.subparser.add_parser('quit')
        self.subparser.add_parser('restart')
        self.subparser.add_parser('command')
        self.mode_parser=self.subparser.add_parser('mode')

        self.mode_parser.add_argument('-m', '--mode')
        self.mode_parser.add_argument('-a', '--action')
        self.mode_parser.add_argument('-p', '--port', type=int)

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

    def portAction(self, port, action, slots={}):

        socket = zmq.Context().socket(zmq.PUSH)
        socket.connect(f'tcp://localhost:{port}')
        slots['action']=action
        socket.send_json(slots)

    def modeAction(self, mode, action, slots={}):

        slots['action']=action
        cmd={'command':'setModeAction', 'mode':mode, 'slots':slots}
        self.socket.send_json(cmd)
        print(self.socket.recv_json())

    def commandAction(self, action):

        self.socket.send_json({'command':action})
        print(self.socket.recv_json())

    def runApp(self):

        app=Willmann()

        if app.socket:
            app.run()
        else:
            print('An instance of Willmann is already running')

    # TODO: finish & add socket polling in quit

    def run(self):

        args, unknown = self.parser.parse_known_args()
        
        if args.command=='mode':

            slots={}
            for i in range(0, len(unknown), 2):
                slots[unknown[i][2:]]=unknown[i+1]

            if args.port:
                self.setSocket(kind='port')
                self.portAction(
                        args.port, args.action, slots)
            elif args.mode:
                self.setSocket(kind='main')
                self.modeAction(
                        args.mode, args.action, slots)

        else:
            self.setSocket(kind='main')

            if args.command=='run':
                self.runApp()
            elif args.command=='quit':
                self.commandAction('quit')
            elif args.command=='restart':
                self.commandAction('restart')
            elif args.command=='command':
                self.mainAction(args.command)

if __name__=='__main__':

    cli = WillmannCLI()
    cli.run()
