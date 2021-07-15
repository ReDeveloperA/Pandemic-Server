#! /usr/bin/python
# -*- coding:utf-8 -*-

import socketserver
import hashlib
from ByteReader import *
from MessageParser import *
from ReturnJobs import *
from CommonData import *
from threading import Lock

class RequestHandler(socketserver.StreamRequestHandler):
    _lock = None
    _commonData = None

    def setup(self):
        print('')
        print('start setup!----------------------------------------------------')
        self.returnJobs = {
                RequestNo.MAKE_GAME             : ReturnJobs.makeGame,
                RequestNo.JOIN_GAME             : ReturnJobs.joinGame,
                RequestNo.GET_CONNECTION_STATUS : ReturnJobs.getConnectionStatus,
                RequestNo.UPDATE_GAME           : ReturnJobs.updateGame,
                RequestNo.GET_GAME_DATA         : ReturnJobs.getGameData
                }

        ret = socketserver.StreamRequestHandler.setup(self)
        print('end setup!----------------------------------------------------')

        return ret

    def handle(self):
        print('')
        print('')
        print('start handler!----------------------------------------------------')

        mp = MessageParser()
        data = self.rfile.readline().strip()
        if not mp.parse(data):
            fail_data = bytes()
            fail_data += RequestNo.NONE.encode('utf-8')
            fail_data += ReturnCode.FAIL.encode('utf-8')
            fail_data += "\n".encode('utf-8')
            self.wfile.write(fail_data)
            print('end handler!----------------------------------------------------')
            return

        print('Received Message : ')
        print('-------------------------------------')
        print('reqestNo')
        print(mp.requestNo)
        print('gameNo')
        print(mp.gameNo)
        #print('gameData')
        #print(mp.gameData)
        print('-------------------------------------')

        RequestHandler._lock.acquire()
        sendData = self.returnJobs[mp.requestNo](mp, RequestHandler._commonData)
        RequestHandler._lock.release()

        print('Send Message : ')
        print('-------------------------------------')
        print(sendData[0:100])
        #print(sendData) # for debug
        print('-------------------------------------')

        self.wfile.write(sendData)

        # for debug
        #print('Currnt data : ')
        #print('-------------------------------------')
        #print(RequestHandler._commonData.gameNoList)
        #print(RequestHandler._commonData.playerDict)
        #print(RequestHandler._commonData.gameDataDict)
        #print('-------------------------------------')
        # for debug

        print('end handler!------------------------------------------------------')
        print('')
        print('')

        return

if __name__ == '__main__':
    import socket

    RequestHandler._lock = Lock()
    RequestHandler._commonData = CommonData()

    address = ('112.34.21.12', 31526) # カーネルにポート番号を割り当てさせる
    server = socketserver.ThreadingTCPServer(address, RequestHandler)
    server.serve_forever()

    # クリーンアップ
    server.socket.close()
    input('server closed')


