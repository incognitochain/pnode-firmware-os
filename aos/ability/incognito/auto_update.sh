#!/bin/sh bash 
timeUp=$(date "+%Y-%m-%d %H:%M:%S")
echo $timeUp

current_latest_tag=$(docker ps  | awk '{print $2}' | grep "incognito-mainnet")

tags=`curl -X GET https://registry.hub.docker.com/v1/repositories/incognitochain/incognito-mainnet/tags  | sed -e 's/[][]//g' -e 's/"//g' -e 's/ //g' | tr '}' '\n'  | awk -F: '{print $3}' | sed -e 's/\n/;/g'`

sorted_tags=($(echo ${tags[*]}| tr " " "\n" | sort -rn))

latest_tag=${sorted_tags[0]}

if [ "$current_latest_tag" != "incognitochain/incognito-mainnet:$latest_tag" ]
then 
  if [ "$current_latest_tag" == "" ]
  then
    sudo rm -r inco-data/
    sudo rm -r inco-eth-mainnet-data/
  fi
  #update script if need.
  qrcodeValue=($(jq -r '.qrcode' /home/nuc/aos/data/qrcode.json))
  curl -X GET http://localhost:5000/restart-node?qrcode=$qrcodeValue
  #bash "ability/incognito/start.sh"
else
  echo "currently dont update"
fi

  