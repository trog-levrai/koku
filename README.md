# koku
Our own crypto-currency made in Python/OpenCL!

You can see the client options with

```shell
./client.py --help
```

First, you will need to generate a key with the command

```shell
./client --key
```

This will generate .Koku.pem file. Don't lose it otherwise you won't be able to spend the money sent to this key.
This command will also prompt your address, you can find it again at any moment with

```shell
./client --address
```

To launch the miner ina  daemon. Please note that you need to have generated a key first.
```shell
./miner.py
```

The daemon will output the logging in /tmp/koku.log.

To stop the miner:

```shell
./miner.py -s
```

Please note that both client ans miner communicate on the same port, Thus it is impossible to use them at the sale time.

To send 10 to adress XXX, the following command must be used.

```shell
./client.py -d XXX -A 10
```
