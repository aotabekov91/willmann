import os
import zmq
import argparse

from plugin import Plug

class ModerCLI(Plug):

    def __init__(self):
        super(ModerCLI, self).__init__()

        self.setParser()

    def setParser(self):
        self.parser=argparse.ArgumentParser()
        self.parser.add_argument('-p', '--port', type=int)
        self.parser.add_argument('-a', '--actions', action='append')
        self.parser.add_argument('-r', '--handler', action='append')

    def setListener(self):
        if self.port:
            self.socket = zmq.Context().socket(zmq.REQ)
            self.socket.connect(f'tcp://localhost:{self.port}')

    def setModeConnection(self, port):
        socket = zmq.Context().socket(zmq.PUSH)
        socket.connect(f'tcp://localhost:{port}')
        return socket

    def runModeAction(self, actions, port):
        socket=self.setModeConnection(port)
        for mode_action in actions:
            socket.send_json({'command': mode_action})

    def runModeActionParent(self, actions):
        if self.port:
            for mode_action in actions:
                tmp=mode_action.split('_')
                mode_name, action_name=tmp[0], tmp[-1]

                try:
                    cmd={'command':'setModeAction',
                         'mode_name':mode_name,
                         'mode_action': mode_action
                         }
                    self.socket.send_json(cmd)
                    print(self.socket.recv_json())
                except:
                    pass

    def runModerAction(self, actions):

        if self.port:
            for action in actions:

                try:

                    self.socket.send_json({'command':action})
                    print(self.socket.recv_json())

                except:
                    pass

    def run(self):
        args=self.parser.parse_args()
        if args.actions and args.port:
            self.runModeAction(args.actions, args.port)
        elif args.actions:
            self.runModeActionParent(args.actions)
        elif args.handler:
            self.runModerAction(args.handler)

if __name__ == '__main__':
    r=ModerCLI()
    r.run()
