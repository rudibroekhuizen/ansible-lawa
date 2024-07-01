#!/bin/bash
systemd-notify --ready
MESSAGE="System is going to reboot in 5 minutes for maintenance. Cancel the reboot with: sudo systemctl stop maintenance-reboot.service"
if [ -f /var/run/reboot-required ]; then
    systemd-notify --status="Initiating reboot"
    echo "Initiating system reboot, requested for packages below:"
    if [ -f /var/run/reboot-required.pkgs ];then
        cat /var/run/reboot-required.pkgs
    else
        echo "No packages specified"
    fi
    echo "$MESSAGE" | wall -n 2>&1 > /dev/null
    sleep 300
    systemctl reboot
else
    echo "No reboot required"
fi
