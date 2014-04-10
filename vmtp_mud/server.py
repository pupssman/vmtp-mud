"""
This is server module for VMTP MUD

It contains a core entry point ``main`` that is used to run server -- it blocks indefinitely

@author: pupssman
"""

import xmlrpc.server

import logging
logging.basicConfig(level=logging.INFO)


class GameServer:
    """
    Implements actual MUD server
    """


def main():
    # FIXME: that needs to be determined properly
    host = '127.0.0.1'
    port = 8081

    server = xmlrpc.server.SimpleXMLRPCServer((host, port))

    server.register_instance(GameServer())

    logging.info("MUD serving at enpoint http://{0}:{1}/".format(host, port))
    logging.info("Press Ctrl-C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Stopped")


if __name__ == '__main__':
    main()
