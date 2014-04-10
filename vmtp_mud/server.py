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


class LinearDungeon:
    """
    A simple linear dungeon, consisting of several lined up rooms, like:

    Entrance -> Room_1 -> Room_2

    :arg rooms: the ones consisting this dungeon
    """

    def __init__(self, *rooms):
        self.rooms = list(rooms)

        for p, n in zip(self.rooms[:-1], self.rooms[1:]):
            p.add_door(n)
            n.add_door(p)

    def entrance(self):
        """
        Returns this dungeon's entrance, i.e. the first room
        """

        return self.rooms[0]


class Room:
    """
    Represents a room in a dungeon.

    :arg description: a player-visible description of a room, like 'big room' or 'narrow corridor'
    """
    def __init__(self, description="basic room"):
        self.description = description
        self.neighbours = []

    def add_door(self, room):
        """
        Adds given ``room`` as a neighbour
        """

        self.neighbours.append(room)

    def where_leads(self, exit_num):
        return exit_num < len(self.neighbours) and self.neighbours[exit_num] or None

    def describe(self):
        return "{0}. There are {1} exits.".format(self.description, len(self.neighbours))


class Player:
    """
    Represents PC.
    """
    def __init__(self, name):
        self.name = name
        self.location = None

    def look(self):
        """
        Reports current surroundings in text form
        """
        if not self.location:
            return "You appear to be nowhere"
        else:
            return "You are in a {}".format(self.location.describe())

    def take_exit(self, exit_num):
        """
        Take a given exit from the current location, if possible.

        :arg exit_num: number of exit, starting from 1

        Returns user message.
        """
        if self.location and self.location.where_leads(exit_num - 1):
            self.location = self.location.where_leads(exit_num - 1)
            return "You have passed a doorway"
        else:
            return "This is impossible"

    def __repr__(self):
        return "<Player name='{0}'>".format(self.name)


DUNGEON = LinearDungeon(Room('small entrance chamber'),
                        Room('long hallway'),
                        Room('large cavern'),
                        Room('dreadly treasury'))


class GameServer:
    """
    Implements actual MUD server

    :arg name: a ``Name`` of this server
    """

    def __init__(self, name):
        self.name = name
        self.dungeon = DUNGEON

        self.players = {}

    def look(self, token):
        """
        Performs a mud's classical ``look`` -- report current surroundings for a given player
        """
        if token not in self.players:
            raise ValueError('Unknown player')
        return self.players[token].look()

    def take_exit(self, token, exit_nmb):
        """
        Player tries to move through given exit
        """
        if token not in self.players:
            raise ValueError('Unknown player')
        return self.players[token].take_exit(exit_nmb)

    def login(self):
        """
        Called on start of the game

        Registers a new player within current session and returns a dict with following attributes:
          -- server_name: a name of server so player gets to know where he has just logged to
          -- player_name: a freshly generated name for this player
          -- player_token: a unique token for the current user session. This is required to do any operations.

        Returns a map with ``server_name`` and ``player_name`` entries.
        """

        player = Player("Mighty {}".format(''.join(random.sample(string.ascii_letters, 5))))
        token = str(uuid.uuid4())

        self.players[token] = player

        player.location = self.dungeon.entrance()

        logging.info("Player {} has logged on".format(player))

        return {"server_name": self.name,
                "player_name": player.name,
                "player_token": token}

    def logoff(self, token):
        if token in self.players:
            player = self.players.pop(token)
            logging.info("Player {} has logged off".format(player))
        else:
            raise ValueError('Unknown player')

        return True  # cause we can't return None


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
