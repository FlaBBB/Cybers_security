#!/bin/bash

cd /home/user/blockchain/
/home/user/.foundry/bin/cast balance 0x710ACb69aCa6aD658633A50D5e0CFFA52Dc7Bf07 --rpc-url http://127.0.0.1:8545 | grep 5

if [ $? -eq 0 ]; then

    /home/user/.foundry/bin/forge script ./script/Minaminao.s.sol \
        --rpc-url http://127.0.0.1:8545 \
        --private-key <PRIVATE_KEY> \
        --broadcast \
        --slow

fi
