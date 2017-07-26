#!/usr/bin/env python3

import os
import time
import signal
import logging
from common.address import *
from common.block import Block
from daemonize import Daemonize
from optparse import OptionParser
from common.p2p2 import KokuStruct
from common.block import checkChain
from common.p2p2 import KokuNetwork
from common.p2p2 import KokuMessageType
from common.transaction import Transaction

pid = "/tmp/koku.pid"
sk = None
addr = ''
chain = [ Block(None, None) ]
net = None

def getBlock(net, hashcode):
    #get the block to corresponding hashcode from net
    return 0

def updateChain(net):
    #Pour l'instant on save pas la chain
    #Get last from net instead of None
    block = None
    tmp = []
    while not block.prev is None:
        tmp.append(block)
        block = getBlock(net, block.prev)
    chain = chain + tmp[::-1]
    return checkChain(chain)

def main():
    #J'ai ajouté logging ici pour que le network puisse en faire. C'est dans /tmp/koku.log
    #Ici il faut récupérer pleins de peers, je pense que c'est bon.
    #net.broadcastMessage(KokuMessageType.GET_ADDR, [])
    logging.info('Peer is fetching addresses')
    #while not updateChain(net):
    #    logging.error('An error in the downloaded chain has been detected!')
    while True:
        #mine new block
        #if new block add to chain
        #else propagate it
        time.sleep(1)

if __name__ == "__main__":
    parser = OptionParser(description="This script is useed to mine the Koku crypto-currency. The logs are located in /tmp/koku.log")
    parser.add_option("-k", "--key", dest="key", help="generate a new keypair (will erease any existing in the same directory)", action="store_true", default=False)
    parser.add_option("-s", "--stop", dest="stop", help="stops the daemon", action="store_true", default=False)
    args, trash = parser.parse_args()

    if args.key:
        print("Your address is:", genKey())
    else:
        logging.basicConfig(
            filename='/tmp/koku.log',
            level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s',
        )
        daemon = Daemonize(app="koku_miner", pid=pid, action=main)
        if args.stop:
            with open(pid, 'r') as f:
                os.kill(int(f.read()), signal.SIGTERM)
                logging.info('Daemon stopped')
        else:
            with open('.Koku.pem', 'rb') as f:
                sk = ecdsa.SigningKey.from_pem(f.read())
                addr = getAddr(sk.get_verifying_key())
                logging.info('Daemon is starting')
                logging.info('Daemon is using address: ' + addr)
                net = KokuNetwork('miner', logging)
                daemon.start()
