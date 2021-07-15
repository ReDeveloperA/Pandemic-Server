#! /usr/bin/python
# -*- coding:utf-8 -*-
from ByteReader import *

class ReturnCode():
    NONE = "0"
    SUCCESS = "1"          # 成功
    GAME = "2"             # ゲーム中
    FULL = "3"             # 部屋番号がいっぱい
    NOT_FOUND = "4"        # 部屋番号が見つからない
    DUP_ROLE = "5"         # 役割重複
    DUP_GAME_NO = "6"      # ゲーム番号重複
    FULL_PLAYER = "7"      # ゲーム番号重複
    CONNECTION_WAIT = "8"  # 接続待機中
    FAIL = "9"             # 失敗

class RequestNo():
    NONE = "00"
    MAKE_GAME = "01"             # ゲーム作成
    JOIN_GAME = "02"             # ゲーム参加
    GET_CONNECTION_STATUS = "03" # 接続状況取得
    UPDATE_GAME = "04"            # ゲーム更新
    GET_GAME_DATA = "10"         # ゲームデータ取得

class PandemicRole():
    OPERATION_EXPERT = "0"
    MEDIC = "1"
    RESEARCHER = "2"
    SCIENTIST = "3"
    DISPATCHER = "4"
    QUARANTINE_SPECIALIST = "5"
    CONTINGENCY_PLANNER = "6"
    NO_PLAYER = "7"

class MessageParser():
    def __init__(self):
        self.requestNo = RequestNo.NONE
        self.retCode = ReturnCode.FAIL
        self.role = PandemicRole.NO_PLAYER
        self.gameNo = None
        self.gameData = None

    def parse(self, byteData):
        reader = ByteReader(byteData)

        # メッセージ番号取得
        self.requestNo = reader.getString(2, 'utf-8')
        if self.requestNo == None:
            self.retCode = ReturnCode.FAIL
            return False


        if self.requestNo == RequestNo.MAKE_GAME:
            # ゲーム作成
            self.role = MessageParser.GetRole(reader.getString(1, 'utf-8'))
            if self.role != PandemicRole.NO_PLAYER:
                self.retCode = ReturnCode.SUCCESS
                return True

        elif self.requestNo == RequestNo.JOIN_GAME:
            # ゲーム参加
            self.gameNo = reader.getString(16, 'utf-8')
            self.role = MessageParser.GetRole(reader.getString(1, 'utf-8'))
            if self.gameNo != None and self.role != PandemicRole.NO_PLAYER:
                self.retCode = ReturnCode.SUCCESS
                return True

        elif self.requestNo == RequestNo.GET_CONNECTION_STATUS:
            # 接続状況取得
            self.gameNo = reader.getString(16, 'utf-8')
            if self.gameNo != None:
                self.retCode = ReturnCode.SUCCESS
                return True

        elif self.requestNo == RequestNo.UPDATE_GAME:
            # ゲーム更新
            self.gameNo = reader.getString(16, 'utf-8')
            self.gameData = reader.getString(808, 'utf-8')
            if self.gameNo != None and self.gameData != None:
                self.retCode = ReturnCode.SUCCESS
                return True

        elif self.requestNo == RequestNo.GET_GAME_DATA:
            # ゲームデータ取得
            self.gameNo = reader.getString(16, 'utf-8')
            if self.gameNo != None:
                self.retCode = ReturnCode.SUCCESS
                return True

        return False

    def GetRole(roleStr):
        if roleStr != None:
            if roleStr == PandemicRole.OPERATION_EXPERT:
                return PandemicRole.OPERATION_EXPERT
            if roleStr == PandemicRole.MEDIC:
                return PandemicRole.MEDIC
            if roleStr == PandemicRole.RESEARCHER:
                return PandemicRole.RESEARCHER
            if roleStr == PandemicRole.SCIENTIST:
                return PandemicRole.SCIENTIST
            if roleStr == PandemicRole.DISPATCHER:
                return PandemicRole.DISPATCHER
            if roleStr == PandemicRole.QUARANTINE_SPECIALIST:
                return PandemicRole.QUARANTINE_SPECIALIST
            if roleStr == PandemicRole.CONTINGENCY_PLANNER:
                return PandemicRole.CONTINGENCY_PLANNER

        return PandemicRole.NO_PLAYER

