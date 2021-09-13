#!/bin/sh bash 
timeUp=$(date "+%Y-%m-%d %H:%M:%S")
echo $timeUp
run()
{
  validator_key=xxx
  bootnode="mainnet-bootnode.incognito.org:9330"
  is_shipping_logs=1
  latest_tag=$1
  current_tag=$2
  data_dir="inco-data"
  eth_data_dir="inco-eth-mainnet-data"
  logshipper_data_dir="logshipper-mainnet-data"


  if [ -z "$node_port" ]; then
    node_port="9433";
  fi
  if [ -z "$rpc_port" ]; then
    rpc_port="9334";
  fi

  docker -v || bash -c "wget -qO- https://get.docker.com/ | sh"

  if [ ! -d "$PWD/${eth_data_dir}" ]
  then
    mkdir $PWD/${eth_data_dir}
    chmod -R 777 $PWD/${eth_data_dir}
  fi

  docker rm -f inc_mainnet
  docker rm -f eth_mainnet
  if [ "$current_tag" != "" ]
  then
    docker image rm -f incognitochain/incognito-mainnet:${current_tag}
  fi

  docker pull incognitochain/incognito-mainnet:${latest_tag}
  docker network create --driver bridge inc_net || true

  docker run -ti --restart=always --net inc_net -d -p 8545:8545  -p 30303:30303 -p 30303:30303/udp -v $PWD/${eth_data_dir}:/home/parity/.local/share/io.parity.ethereum/ --name eth_mainnet  parity/parity:stable --light --jsonrpc-interface all --jsonrpc-hosts all  --jsonrpc-apis all --mode last --base-path=/home/parity/.local/share/io.parity.ethereum/

  docker run --restart=always --net inc_net -p $node_port:$node_port -p $rpc_port:$rpc_port -e NODE_PORT=$node_port -e RPC_PORT=$rpc_port -e BOOTNODE_IP=$bootnode -e GETH_NAME=eth_mainnet -e MININGKEY=${validator_key} -e TESTNET=false -v $PWD/${data_dir}:/data -d --name inc_mainnet incognitochain/incognito-mainnet:${latest_tag}

  #post updated_success_full_to_node_visualize_logs 
  qrcodeValue=($(jq -r '.qrcode' /home/nuc/aos/data/qrcode.json))
  
  curl -X POST -H 'Content-type: application/json' --data '{"text":"node-'$qrcodeValue'-miningkey-'$validator_key'-update-complete:'$latest_tag'"}' https://hooks.slack.com/services/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
  
  if [ $is_shipping_logs -eq 1 ]
  then
    if [ ! -d "$PWD/${logshipper_data_dir}" ]
    then
      mkdir $PWD/${logshipper_data_dir}
      chmod -R 777 $PWD/${logshipper_data_dir}
    fi
    docker image rm -f incognitochain/logshipper:1.0.0
    docker run --restart=always -d --name inc_logshipper -e RAW_LOG_PATHS=/tmp/*.txt -e JSON_LOG_PATHS=/tmp/*.json -e LOGSTASH_ADDRESSES=34.94.14.147:5000 --mount type=bind,source=$PWD/${data_dir},target=/tmp --mount type=bind,source=$PWD/${logshipper_data_dir},target=/usr/share/filebeat/data incognitochain/logshipper:1.0.0
  fi
}

#current_latest_tag=""  
current_latest_tag=$(docker ps  | awk '{print $2}' | grep "incognito-mainnet")

#format clear old version
if [ "$current_latest_tag" == "incognitochain/incognito-mainnet:20191108_1" ]
then  
  sudo rm -r /home/nuc/aos/inco-data/
  sudo rm -r /home/nuc/aos/inco-eth-mainnet-data/
  sudo rm -r /home/nuc/aos/logshipper-mainnet-data
fi 

FILEDBV2=/home/nuc/aos/data/dbv2.txt
if [ ! -f "$FILEDBV2" ]; then
    echo "$FILEDBV2 does not exist, remove dbv1."

    docker rm -f inc_mainnet
    docker rm -f eth_mainnet
    docker rm -f inc_logshipper
    sudo rm -r /home/nuc/aos/inco-data/
    sudo rm -r /home/nuc/aos/inco-eth-mainnet-data/
    sudo rm -r /home/nuc/aos/logshipper-mainnet-data
    sudo touch /home/nuc/aos/data/dbv2.txt

fi


tags=`curl -X GET https://registry.hub.docker.com/v1/repositories/incognitochain/incognito-mainnet/tags  | sed -e 's/[][]//g' -e 's/"//g' -e 's/ //g' | tr '}' '\n'  | awk -F: '{print $3}' | sed -e 's/\n/;/g'`

sorted_tags=($(echo ${tags[*]}| tr " " "\n" | sort -rn))
latest_tag=${sorted_tags[0]}

if [ "$current_latest_tag" != "$latest_tag" ]
then
  run $latest_tag $current_latest_tag
  current_latest_tag=$latest_tag
fi
 