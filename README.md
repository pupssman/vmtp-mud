VMTP MUD
========

A learning project in Python -- a **Multi-User Dungeon**


It is designed to be an easy-to-build modular Mult-User game so many people can contribute to the process.

The client-server protocol is built atop **XML-RPC**.


Usage
=====

It consists of two parts -- a *client* and a *server*.

One requires a running server to connect -- launch it with provided entry point ``vmtp-mud-server`` or via running **server.py** directly.

Then, launch ``vmpt-mud --server https://<server_host>:<server_port>/`` and use supplied directions.