import time
import struct
import random
import hashlib
from common.merkle import Merkle

import logging

class Block:

    def __init__(self, prev, root, idBlock):
        self.prev = prev
        self.root = root
        self.id = idBlock
        self.bits = 20
        self.pad = 0
        self.difficulty = 2**11
        self.time = int(time.time())
        self.transactions = []

    #Sets the transactions list of this block.
    #If the Merkle root matches returns True. Returns false otherwise
    def setTransactions(self, transactions):
        #First we get the list of transactions hashes
        hashlist = []
        for t in transactions:
            m = hashlib.sha256()
            m.update(t.getPack())
            hashlist.append(m.digest())

        #Then we can compute the Merkle root given by those hashes
        merkle = Merkle(hashlist)
        self.transactions = transactions
        return True

    #Returns a tuple indicating if this block is the last one where addr spent
    #The second term of the tuple is the amount earned by addr in this block
    def getIncome(self, addr):
        last = False
        total = 0
        for t in self.transactions:
            if t.dest == addr and t.checkSig():
                total += t.amount
            elif t.sender == addr and t.checkSig():
                total += t.utxo
                last = True
        return (last, total)

    def getPack(self):
        return struct.pack('32s32s5I', self.prev, self.root, self.id, self.bits, self.pad, self.time, self.difficulty)

    def unpack(self, buff):
        self.prev, data = struct.unpack('32s', buff[:32])[0], buff[32:]
        self.root, data = struct.unpack('32s', data[:32])[0], data[32:]
        obj = struct.unpack('3I', data)
        self.id = obj[0]
        self.bits = obj[1]
        self.pad = obj[2]

    def getHash(self, nounce = 0):
        self.pad += nounce
        m = hashlib.sha256()
        m.update(self.getPack())
        self.pad -= nounce
        return m.digest()

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    def getDifficulty(self):
        return self.difficulty

    def getTime(self):
        return self.time

    def updateTime(self):
        self.time = int(time.time())

def checkChain(logger, chain):
    return True
    for i in range(len(chain))[::-1]:
        h = chain[i].getHash()
        val = int.from_bytes(h[:4], byteorder='little', signed=False)
        if val >= chain[i].difficulty or chain[i].difficulty != getDifficulty(chain[:i]):
            logger.info('val : ' + str(val) + ' diff : ' + str(chain[i].difficulty) + ' getDiff : ' + str(getDifficulty(chain[:i])))
            return False
    return True

def getAmountAvailable(addr, chain):
    rev = chain[::-1]
    i = 0
    ans = 0
    last = False
    while i < len(rev) and not last:
        last, amount = rev[i].getIncome(rev[i])
        ans += amount
        i += 1
    return ans

def getDifficulty(chain):
    return 2**8
    if len(chain) < 5:
        return 2 ** 10
    delta = chain[-1].getTime() - chain[-5].getTime()
    prevDifficulty = chain[-1].getDifficulty()
    return int(prevDifficulty * delta / 75.)
