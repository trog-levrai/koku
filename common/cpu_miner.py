from multiprocessing import Pool
from copy import copy
import common.block
import logging
import hashlib
import os

class cpu_miner:

    def __init__(self, logging):
        self.logging = logging
        self.batch = 2**20
        self.mining = True
        self.not_interrupted = True

    def set_block(self, block):
        self.block = block

    def interrupt(self):
        self.not_interrupted = False
        self.logging.info('Interrupted batch')

    def compute_hashes(self, net):
        i = 0
        length = int(self.batch / os.cpu_count())
        while self.not_interrupted:
            self.logging.info('Starting batch ' + str(i))
            self.block.updateTime()
            with Pool(None) as p:
                self.block.pad = i * self.batch
                vals = p.map(try_pad, [(copy(self.block), i * length, length) for i in range(os.cpu_count())])
                val = []
                for v in vals:
                    val += v
                int_miner = net.getInteruptMiner()
                self.logging.info('int ' + str(int_miner))
                if int_miner:
                    self.interrupt()
                    net.resetInteruptMiner()
                    return (self.block, False)

                for j, v in enumerate(val):
                    if v < self.block.difficulty:
                        self.block.pad = i * self.batch + j
                        return (self.block, True)

                i = i+1 if (i+1) * self.batch < 2**32 else 0

        return (self.block, False)

def try_pad(arg):
    block, begin, length = arg
    ans = []
    for i in range(length):
        m = block.getHash(begin + i)
        ans.append(int.from_bytes(m[:4], byteorder='little', signed=False))
    return ans
