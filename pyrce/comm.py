#!/usr/bin/env python
# -*- coding: utf-8 -*-
#     
#     comm.py
#     
#     This file is part of the RoboEarth Cloud Engine pyrce client.
#     
#     This file was originally created for RoboEearth
#     http://www.roboearth.org/
#     
#     The research leading to these results has received funding from
#     the European Union Seventh Framework Programme FP7/2007-2013 under
#     grant agreement no248942 RoboEarth.
#     
#     Copyright 2012 RoboEarth
#     
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#     
#     http://www.apache.org/licenses/LICENSE-2.0
#     
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#     
#     \author/s: Dominique Hunziker 
#     
#     

# twisted specific imports
from autobahn.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol

# Custom package imports
import sys                          ### TODO:
sys.path.append('../framework')     ### TEMPORARY FIX

from client.assembler import MessageAssembler


class RCERobotProtocol(WebSocketClientProtocol):
    def __init__(self, connection):
        self._connection = connection
        self._assembler = MessageAssembler(self, 60)
    
    def onConnect(self, _):
        self._assembler.start()
        self._connection.registerConnection(self)
    
    def onMessage(self, msg, binary):
        self._assembler.processMessage(msg, binary)
    
    def processCompleteMessage(self, msg):
        self._connection.receivedMessage(msg)
    
    def onClose(self, *_):
        self._connection.unregisterConnection(self)
        self._assembler.stop()


class RCERobotFactory(WebSocketClientFactory):
    def __init__(self, url, connection):
        WebSocketClientFactory.__init__(self, url)
        self._connection = connection
    
    def buildProtocol(self, addr):
        p = RCERobotProtocol(self._connection)
        p.factory = self
        return p
