"""
This is server module for VMTP MUD

It contains a core entry point ``main`` that is used to run server -- it blocks indefinitely

@author: pupssman
"""

import xmlrpc.server

import logging
import random
import string
import uuid
logging.basicConfig(level=logging.INFO)


class GameServer:
    """
    Implements actual MUD server

    :arg name: a ``Name`` of this server
    """

    def __init__(self, name):
        self.name = name

        self.players = {}

    def login(self):
        """
        Called on start of the game

        Registers a new player within current session and returns a dict with following attributes:
          -- server_name: a name of server so player gets to know where he has just logged to
          -- player_name: a freshly generated name for this player
          -- player_token: a unique token for the current user session. This is required to do any operations.

        Returns a map with ``server_name`` and ``player_name`` entries.
        """

        name = "Player_{}".format(''.join(random.sample(string.ascii_letters, 5)))
        token = str(uuid.uuid4())

        self.players[token] = name

        logging.info("Player <{}> has logged on".format(name))

        return {"server_name": self.name,
                "player_name": name,
                "player_token": token}

    def logoff(self, token):
        if token in self.players:
            player = self.players.pop(token)
            logging.info("Player <{}> has logged off".format(player))
        else:
            logging.warn("Received logoff for unknown token <{}>".format(token))

        return True  # cas we cant return None


def main():
    # FIXME: that needs to be determined properly
    host = '127.0.0.1'
    port = 8081

    server = xmlrpc.server.SimpleXMLRPCServer((host, port))

    server.register_instance(GameServer('Nowhere'))

    logging.info("MUD serving at enpoint http://{0}:{1}/".format(host, port))
    logging.info("Press Ctrl-C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Stopped")


if __name__ == '__main__':
    main()
