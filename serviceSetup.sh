#!/bin/bash

echo "Creating new service DryerPi.service"
sudo touch /lib/systemd/system/DryerPi.service

sudo cat > /lib/systemd/system/DryerPi.service << EOF
[Unit]
Description=DryerPi
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /home/pi/DryerPi/dryerPi.py

[Install]
WantedBy=multi-user.target

EOF

sudo chmod 644 /lib/systemd/system/DryerPi.service

echo "Restarting daemon service"
sudo systemctl daemon-reload
pid=$!
wait $!

echo "Enabling DryerPi.service"
sudo systemctl enable DryerPi.service