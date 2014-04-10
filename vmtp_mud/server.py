"""
This is server module for VMTP MUD

It contains a core entry point ``main`` that is used to run server -- it blocks indefinitely

@author: pupssman
"""

import xmlrpc.server

import logging
import random
import string
logging.basicConfig(level=logging.INFO)


class GameServer:
    """
    Implements actual MUD server

    :arg name: a ``Name`` of this server
    """

    def __init__(self, name):
        self.name = name

    def start(self):
        """
        Called on start of the game

        Returns a map with ``server_name`` and ``player_name`` entries.
        """
        return {"server_name": self.name,
                "player_name": "Player_{}".format(''.join(random.sample(string.ascii_letters, 5)))}


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
