"""
This module holds smoke tests.

Run with py.test
"""
import pytest
import multiprocessing as mp

from vmtp_mud.server import main as srv_main
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


def test_login_works(server):
    assert server.login()
