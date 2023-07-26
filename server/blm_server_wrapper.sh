#!/bin/bash

set +e #otherwise the script will exit on error
elementIn () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}


host=$1
port=$2

if [[ -z $host ]]
then
    exec >&2; echo "Must supply a host"; exit 1
fi

if [[ -z $port ]]
then
    exec >&2; echo "Must supply a port number"; exit 1
fi

if ! [[ "$port" =~ ^[0-9]+$ ]]
then
    exec >&2; echo "Port number is not a number"; exit 1
fi

if ! ((port >= 1024 && port <= 65535))
then
    exec >&2; echo "Port number must be between 1024 and 65535"; exit 1
fi

declare -a listening_ports=(`ss -tulwn |sed 1d |tr -s ' ' |cut -d ' ' -f 5|sed 's/.*://'`)

if elementIn "$port" "${listening_ports[@]}"
then
    exec >&2; echo "Port already in use"; exit 1
fi

while true
do
    python3 blinkloadmem_server.py $host $port
    sleep 2
done
