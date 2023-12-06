#!/bin/bash
nitrogen --restore &
picom &
dte(){
    D2B=({0..1}{0..1}{0..1}{0..1}{0..1}{0..1})
    hour="$(date '+%H')"
    min="$(date '+%M')"
    time=${D2B[$hour]}:${D2B[$min]}
    date="$(date '+%Y-%m-%d')"
    dte=" $date | $time "
    #dte="$(date '+%Y-%m-%d | %H:%M')"
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
    xsetroot -name " $(mem) |$(dte)"
    sleep 1m
done &

xrandr --output VGA-1 --mode 2560x1440
#exec dbus-launch dwm
while type dwm>/dev/null ;do dwm && continue || break ;done
