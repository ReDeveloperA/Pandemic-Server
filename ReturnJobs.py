#! /usr/bin/python
# -*- coding:utf-8 -*-

from MessageParser import *
from CommonData import *
import random, string

class ReturnJobs():
    def randomname(n):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

    # ゲーム作成
    def makeGame(mp, commonData):
        retCode = ReturnCode.FAIL
        gameNo = "0000000000000000"

        if 0 <= int(mp.role) and int(mp.role) <= 6:
            gameNo = ReturnJobs.randomname(16)
            if commonData.addGameNo(gameNo):
                commonData.addPlayer(gameNo, mp.role)
                retCode = ReturnCode.SUCCESS
            else:
                gameNo = "0000000000000000"
                if commonData.errorCode == ErrorCode.MAX_CONNECTION:
                    retCode = ReturnCode.FULL
                elif commonData.errorCode == ErrorCode.DUP_GAME_NO:
                    retCode = ReturnCode.DUP_GAME_NO

        ret = bytes()
        ret += RequestNo.MAKE_GAME.encode('utf-8')
        ret += retCode.encode('utf-8')
        ret += gameNo.encode('utf-8')
        ret += "\n".encode('utf-8')
        return ret

    # ゲーム参加
    def joinGame(mp, commonData):
        retCode = ReturnCode.FAIL
        phase = "0"

        if commonData.addPlayer(mp.gameNo, mp.role):
            retCode = ReturnCode.SUCCESS
            phase = str(commonData.getPlayerNum(mp.gameNo))
        else:
            if commonData.errorCode == ErrorCode.MAX_PLAYER:
                retCode = ReturnCode.FULL_PLAYER
            elif commonData.errorCode == ErrorCode.DUP_ROLE:
                retCode = ReturnCode.DUP_ROLE
            elif commonData.errorCode == ErrorCode.NOT_FOUND_GAME_NO:
                retCode = ReturnCode.NOT_FOUND
            elif commonData.errorCode == ErrorCode.GAME:
                retCode = ReturnCode.GAME
                phase = str(commonData.getPhase(mp.gameNo, mp.role))

        ret = bytes()
        ret += RequestNo.JOIN_GAME.encode('utf-8')
        ret += retCode.encode('utf-8')
        ret += phase.encode('utf-8')
        ret += "\n".encode('utf-8')
        return ret

    # 接続状況取得
    def getConnectionStatus(mp, commonData):
        retCode = ReturnCode.SUCCESS
        player = commonData.getPlayerList(mp.gameNo)

        if player == None:
            retCode = ReturnCode.NOT_FOUND
            player = []

        gameData = commonData.getGameData(mp.gameNo)
        if gameData == None:
            retCode = ReturnCode.NOT_FOUND
        elif gameData != "":
            retCode = ReturnCode.GAME

        ret = bytes()
        ret += RequestNo.GET_CONNECTION_STATUS.encode('utf-8')
        ret += retCode.encode('utf-8')

        for i in range(4):
            if i < len(player):
                ret += player[i].encode('utf-8')
            else:
                ret += PandemicRole.NO_PLAYER.encode('utf-8')

        ret += "\n".encode('utf-8')
        return ret

    # ゲーム更新
    def updateGame(mp, commonData):
        retCode = ReturnCode.SUCCESS

        #ReturnJobs.printGameData(mp.gameData)

        if not commonData.updateGameData(mp.gameNo, mp.gameData):
            if commonData.errorCode == ErrorCode.NOT_FOUND_GAME_NO:
                retCode = ReturnCode.NOT_FOUND
            else:
                retCode = ReturnCode.FAIL

        ret = bytes()
        ret += RequestNo.UPDATE_GAME.encode('utf-8')
        ret += retCode.encode('utf-8')
        ret += "\n".encode('utf-8')
        return ret

    # ゲームデータ取得
    def getGameData(mp, commonData):
        retCode = ReturnCode.SUCCESS
        gameData = commonData.getGameData(mp.gameNo)

        if gameData == None:
            retCode = ReturnCode.NOT_FOUND_GAME_NO
            gameData = "".join(["0" for i in range(808)])
        elif gameData == "":
            retCode = ReturnCode.CONNECTION_WAIT
            gameData = "".join(["0" for i in range(808)])

        #ReturnJobs.printGameData(gameData)

        ret = bytes()
        ret += RequestNo.GET_GAME_DATA.encode('utf-8')
        ret += retCode.encode('utf-8')
        ret += gameData.encode('utf-8')
        ret += "\n".encode('utf-8')

        return ret

    def printGameData(gameData):
        if gameData == None or len(gameData) != 808:
            return

        i = 0
        print("difficulty : "       + gameData[i])
        i += 1
        print("nowPlayer : "        + gameData[i])
        i += 1
        print("turnCounter : "      + gameData[i])
        i += 1
        print("epidemicCounter : "  + gameData[i])
        i += 1
        print("playerNum : "        + gameData[i])
        i += 1
        print("playerDeck : "       + gameData[i : 2 * 59])
        i += 2 * 59
        print("playerDiscard : "    + gameData[i : 2 * 59])
        i += 2 * 59
        print("infectionDeck : "    + gameData[i : 2 * 48])
        i += 2 * 48
        print("infectionDiscard : " + gameData[i : 2 * 48])
        i += 2 * 48
        print("outbrakeMarker : "   + gameData[i])
        i += 1
        print("infectionMarker : "  + gameData[i])
        i += 1

        print("diseaseCubeQuantity : "        + gameData[i : 8])
        i += 8
        print("vaccineMarkerFlags : "         + gameData[i : 4])
        i += 4
        print("researcherStationQuantity : "  + gameData[i])
        i += 1



