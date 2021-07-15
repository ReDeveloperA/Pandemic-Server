#! /usr/bin/python
# -*- coding:utf-8 -*-

class ByteReader():
    def __init__(self, byteData):
        self.byteData = byteData
        self.dataLength = len(byteData)
        self.seek = 0
    
    def getByte(self, length):
        ret = None
        if self.seek + length <= self.dataLength and length > 0:
                ret = self.byteData[self.seek:self.seek + length]
                self.seek += length

        return ret

    def getInt(self, length, order):
        b = self.getByte(length)

        if b:
            b = int.from_bytes(b, order)

        return b

    def getString(self, length, charset):
        b = self.getByte(length)

        if b:
            b = b.decode(charset)

        return b

    def getBoolean(self):
        b = self.getInt(1, 'little')

        if b != None:
            if b == 1:
                b = True
            else:
                b = False

        return b



