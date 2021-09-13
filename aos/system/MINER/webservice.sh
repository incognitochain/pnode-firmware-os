#!/bin/bash
  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/
tmux has-session -t hostservice
if [ $? != 0 ]; then

    tmux new-session -s hostservice -n hostservice -d   
    # tmux new-session -s incognito -n chain -d  
    tmux send-keys -t hostservice:hostservice 'python $HOME/aos/ability/product_control/host_web_service.py' C-m
    
fi
 

 
