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

    def portAction(self, port, args_dict):

        socket = zmq.Context().socket(zmq.PUSH)
        socket.connect(f'tcp://localhost:{port}')
        socket.send_json(args_dict)

    def modeAction(self, mode, args_dict):

        cmd={'command':'setModeAction', 
             'mode':mode, 
             'action': args_dict}
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

    def run(self):

        args=self.parser.parse_args()

        if args.command=='mode':
            if args.port:
                self.setSocket(kind='port')
                self.portAction(args.port, vars(args))
            elif args.mode:
                self.setSocket(kind='main')
                self.modeAction(args.mode, vars(args))

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
