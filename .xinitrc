#!/bin/bash
nitrogen --restore &
picom &
dte(){
    dte="$(date '+%Y-%m-%d | %H:%M')"
    echo -e "$dte"
}

mem() {
    mem="$(free -h | awk '(NR==2){ print $4 }')"
    echo -e "$mem"
}

cputmp(){
    cputmp="$(sed 's/.00/C/' /sys/class/thermal/thermal_zone0/temp)"
    echo -e "$cputmp"
}

ipaddr() {
    ipaddr="$(ip -4 addr show eno1 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')"
    echo -e "$ipaddr"
}
while true
do
    xsetroot -name " $(cputmp) | $(ipaddr) | $(mem) | $(dte) "
    sleep 1m
done &   
exec dbus-launch dwm
