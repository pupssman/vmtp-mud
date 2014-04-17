"""
This module holds smoke tests.

Run with py.test
"""
import pytest
import multiprocessing as mp

from vmtp_mud.server import main as srv_main
from vmtp_mud.client import GameClient

import xmlrpc
import time


@pytest.yield_fixture(scope='function')
def server():
    """
    Starts a server and yields an ``xmlrpc.client.ServerProxy`` targeted there
    """
    process = mp.Process(target=srv_main)
    process.start()

    time.sleep(1)

    # FIXME: that's no good, the port must be changeable
    yield xmlrpc.client.ServerProxy('http://localhost:8081/')

    process.terminate()
    process.join()


@pytest.fixture(scope='function')
def client(server):
    """
    Return patched client ``GameClient`` targeting current ``server``.

    Client has attribute ``messages`` where all the ``client.say`` messages go.
    """
    class PatchedClient(GameClient):
        messages = []

        def say(self, msg):
            self.messages.append(msg)

    return PatchedClient(server)


def test_login_works(server):
    assert server.login()


def test_client_login_welcomes_player(client):
    client.do_login('')

    assert 'Welcome' in client.messages[-1]
