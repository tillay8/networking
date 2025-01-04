#!/bin/bash

messages=(
    "hacking into $@..."
    "penetrating barriers..."
    "reading consent laws for your country..."
    "bypassing consent laws for your country..."
    "bypassing anti-hacking algorithms..."
    "penetrating firewalls..."
    "loading_bar()"
    "leaking your ip addr: $(curl -s ifconfig.me)"
    "leaking your coordinates: $(curl -s ipinfo.io/$(curl -s ifconfig.me) | grep -oP '"loc":\s*"\K[^"]+')"
    "type gaining root access to the mainframe..."
    "activating freaky scripts..."
    "overriding security protocols..."
    "infiltrating the mainframe..."
    "making the system freaky..."
    "extracting sensitive data..."
    "downloading feet pics..."
    "loading_bar()"
    "type penetrating the mainframe..."
    "breaking into private networks..."
    "sending assassins after NSA agents..."
    "erasing system logs..."
    "downloading twitter passwords..."
    "type catching up on r/masterhacker..."
    "loading_bar()"
    "altering system configuration..."
    "removing crucial system files..."
    "taking over third world countries..."
    "system successfully hacked into!"
    "$@ didnt stand a chance lmao"
    "type good job masterhacker"
)

loading_bar() {
    local progress=0 len=50
    while [ $progress -le $len ]; do
        printf "\r[%-${len}s] %d%%" $(printf "#%.0s" $(seq 1 $progress)) $((progress * 2))
        sleep 0.1
        ((progress++))
    done
    echo
}

type() {
    local message="$1"
    for (( i=0; i<${#message}; i++ )); do
        echo -n "${message:$i:1}"
        sleep 0.05
    done
    echo
}

for message in "${messages[@]}"; do
    if [[ "$message" =~ ^type ]]; then
        type "${message#type }"
    elif [[ "$message" =~ \(\)$ ]]; then
        function_name="${message%()}"
        declare -f "$function_name" > /dev/null && $function_name
    elif [[ "$message" =~ ^run ]]; then
        eval "${message#run }"
    else
        echo "$message"
    fi
    sleep $(awk -v min=0.01 -v max=0.4 'BEGIN{srand(); print min + (max-min)*rand()}')
done

