#! /usr/bin/python
# -*- coding:utf-8 -*-

import time

class ErrorCode():
    NONE = 0
    MAX_CONNECTION = 1
    DUP_GAME_NO = 2
    DUP_ROLE = 3
    NOT_FOUND_GAME_NO = 4
    MAX_PLAYER = 5
    GAME = 6

class CommonData():
    def __init__(self):
        self._MAX_CONNECTION = 2
        self.gameNoList = []
        self.playerDict = dict()
        self.gameDataDict = dict()
        self.timestampDict = dict()
        self.errorCode = ErrorCode.NONE

    def addGameNo(self, gameNo):
        if self._MAX_CONNECTION <= len(self.gameNoList):
            removedGameNo = None
            for number in self.gameNoList:
                if time.time() - self.timestampDict[number] >= 180:
                    # 3分以上更新がなければ
                    removedGameNo = number
                    break

            if removedGameNo != None:
                self.gameNoList.remove(removedGameNo)
                del self.playerDict[removedGameNo]
                del self.gameDataDict[removedGameNo]
                del self.timestampDict[removedGameNo]
            else:
                self.errorCode = ErrorCode.MAX_CONNECTION
                return False

        if gameNo in self.gameNoList:
            self.errorCode = ErrorCode.DUP_GAME_NO
            return False

        self.gameNoList.append(gameNo)
        self.playerDict[gameNo] = []
        self.gameDataDict[gameNo] = ""
        self.timestampDict[gameNo] = time.time()
        return True

    def addPlayer(self, gameNo, player):
        if gameNo in self.gameNoList and gameNo in self.playerDict:
            self.timestampDict[gameNo] = time.time() # 更新
            if gameNo in self.gameDataDict and self.gameDataDict[gameNo] != "":
                self.errorCode = ErrorCode.GAME
            elif not player in self.playerDict[gameNo]:
                if len(self.playerDict[gameNo]) < 4:
                    self.playerDict[gameNo].append(player)
                    return True
                else:
                    self.errorCode = ErrorCode.MAX_PLAYER
            else:
                self.errorCode = ErrorCode.DUP_ROLE
        else:
            self.errorCode = ErrorCode.NOT_FOUND_GAME_NO

        return False

    def updateGameData(self, gameNo, gameData):
        if gameNo in self.gameNoList and gameNo in self.gameDataDict:
            self.timestampDict[gameNo] = time.time() # 更新
            self.gameDataDict[gameNo] = gameData
            return True

        self.errorCode = ErrorCode.NOT_FOUND_GAME_NO
        return False

    def getPlayerList(self, gameNo):
        if gameNo in self.gameNoList and gameNo in self.playerDict:
            self.timestampDict[gameNo] = time.time() # 更新
            return self.playerDict[gameNo]
        return None

    def getGameData(self, gameNo):
        if gameNo in self.gameNoList and gameNo in self.gameDataDict:
            self.timestampDict[gameNo] = time.time() # 更新
            return self.gameDataDict[gameNo]
        return ""

    def getPlayerNum(self, gameNo):
        if gameNo in self.gameNoList and gameNo in self.playerDict:
            return len(self.playerDict[gameNo])
        return 0

    def getPhase(self, gameNo, player):
        if gameNo in self.gameNoList and gameNo in self.playerDict:
            if player in self.playerDict[gameNo]:
                return self.playerDict[gameNo].index(player) + 1

        return 0

