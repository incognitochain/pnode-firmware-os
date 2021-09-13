#!/bin/bash

#check new system:
export FIRMWARE_UPDATE__TMP_PATH=$HOME/aos/tmp/system
export TARGET_UPDATE_PATH=$HOME/aos/
export SYSTEM=$TARGET_UPDATE_PATH/system/MINER/system.sh
export WEB=$TARGET_UPDATE_PATH/system/MINER/webservice.sh 
cd $HOME/aos/ability/firmware_update/ && python check_update.py
bash $SYSTEM
#bash $WEB
