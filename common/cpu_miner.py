from multiprocess import Pool
import hashlib
import block

class cpu_miner:

    def __init__(self, block, difficulty):
        self.block = block
        self.block.setDifficulty(difficulty)
        self.bach = 2**20
        self.mining = True

    def stop_mining(self):
        self.mining = False

    def mine(self):
        i = 0
        while self.mining:
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
