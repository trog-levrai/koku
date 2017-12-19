from multiprocessing import Pool
from copy import copy
import logging
import hashlib
import common.block

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

    def compute_hashes(self):
        i = 0
        while self.not_interrupted:
            self.logging.info('Starting batch ' + str(i))
            self.block.updateTime()
            with Pool(None) as p:
                val = p.map(try_pad, [(copy(self.block), x) for x in range(i * self.batch, (i + 1) * self.batch)])

                for j, v in enumerate(val):
                    if v < self.block.difficulty:
                        self.block.pad = i * self.batch + j
                        return (self.block, True)

                i = i+1 if (i+1) * self.batch < 2**32 else 0

        return (self.block, False)

def try_pad(arg):
    block, pad = arg
    block.pad = pad
    m = hashlib.sha256(block.getPack()).digest()
    value = int.from_bytes(m[:4], byteorder='little', signed=False)
    return value
