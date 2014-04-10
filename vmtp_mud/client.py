"""
This is client module for VMTP MUD

It contains a core entry point ``main`` that is used to run actual client

@author: pupssman
"""
import cmd
import logging
import xmlrpc.client

from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)


class GameClient(cmd.Cmd):
    """
    Implements client-side operations
    """

    intro = 'Welcome! Type ? (question mark) to see available commands.'
    prompt = 'MUD >> '

    def __init__(self, rpc_client):
        super(GameClient, self).__init__()

        self.rpc = rpc_client
        self.session_token = None

    def say(self, msg):
        logging.info(msg)

    def do_login(self, _):
        """
        Starts a game session at target server
        """
        if not self.session_token:
            data = self.rpc.login()
            self.session_token = data['player_token']
            self.say("Welcome to the dire world of {1}, {0}!".format(data['player_name'],
                                                                     data['server_name']))
        else:
            self.say("You are already logged in -- nothing to do")

    def do_logoff(self, _):
        """
        Quits a session
        """

        if self.session_token:
            self.rpc.logoff(self.session_token)
            self.say("Goodbye")

            return True
        else:
            self.say("You are not logged in -- nothing to do")


def main():
    parser = ArgumentParser()
    parser.add_argument('--server', dest='server', required=True, help='URL of teh server.')

    args = parser.parse_args()

    GameClient(xmlrpc.client.ServerProxy(args.server)).cmdloop()


if __name__ == '__main__':
    main()
