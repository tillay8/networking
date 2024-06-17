sudo ip link set dev wlan0 down
sudo macchanger -r wlan0
sudo ip link set dev wlan0 up
sleep 1
curl wttr.in | grep "Weather"
ifconfig | grep ether
