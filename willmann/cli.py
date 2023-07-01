import zmq
import argparse
from tendo import singleton

from plugin.plug import Plug
from .willmann import Willmann

class WillmannCLI(Plug):

    def __init__(self):

        super(WillmannCLI, self).__init__()

        self.setParser()

    def setParser(self):

        self.parser=argparse.ArgumentParser()

        self.parser.add_argument('-p', '--port', type=int)
        self.parser.add_argument('-a', '--actions', action='append')
        self.parser.add_argument('-c', '--commands', action='append')

    def setListener(self):

        if self.port:
            self.socket = zmq.Context().socket(zmq.REQ)
            self.socket.connect(f'tcp://localhost:{self.port}')

    def setModeConnection(self, port):

        socket = zmq.Context().socket(zmq.PUSH)
        socket.connect(f'tcp://localhost:{port}')
        return socket

    def portAction(self, actions, port):

        socket=self.setModeConnection(port)
        for action in actions:
            socket.send_json({'action': action})

    def modeAction(self, actions):

        if self.port:
            for action in actions:
                mode=action.split('_')[0]

                cmd={'command':'setModeAction',
                     'mode':mode,
                     'action': action,
                     }
                self.socket.send_json(cmd)
                print(self.socket.recv_json())

    def mainCommand(self, actions):

        if self.port:
            for action in actions:
                self.socket.send_json({'command':action})
                print(self.socket.recv_json())

    def runMain(self):

        try: 

            app=Willmann()
            app.run()

        except singleton.SingleInstanceException:

            print('An instance of Willmann is already runnng')

        except:
            
            raise

    def run(self):

        args=self.parser.parse_args()
        if args.actions and args.port:
            self.portAction(args.actions, args.port)
        elif args.actions:
            self.modeAction(args.actions)
        elif args.commands:
            self.mainCommand(args.commands)
        else:
            self.runMain()
