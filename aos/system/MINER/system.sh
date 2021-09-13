#!/bin/bash

# load apps at startup by default
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/
tmux has-session -t brain
if [ $? != 0 ]; then

    tmux new -s brain -n brain -d  
    # tmux new-session -s incognito -n chain -d  
    tmux send-keys -t brain:brain 'cd $HOME/aos/ && ulimit -s 1024 && ulimit -r 0 && chmod +x system/MINER/brain && system/MINER/brain -b $HOME/aos/data/pr_device.json' C-m
    
fi
 
