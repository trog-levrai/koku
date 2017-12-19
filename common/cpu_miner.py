from multiprocessing import Pool
import logging
import hashlib
import common.block

class cpu_miner:

    def __init__(self, logger):
        self.bach = 2**20
        self.mining = True

    def set_block(self, block):
        self.block = block

    def mine(self):
        i = 0
        while True:
            block.updateTime()
            with Pool(None) as p:
                val = p.map((block, x) for x in range(i * self.batch, (i + 1) * self.batch))

            for j, v in enumerate(val):
                if v < self.block:
                    return i * self.batch + j

            i = i+1 if (i+1) * self.batch < 2**32 else 0

def try_pad(arg):
    block, pad = arg
    block.pad = pad
    m = hashlib.sha256(vlock.getPack()).digest()
    value = int.from_bytes(a, byteorder='little', signed=False)
    return value
